import os
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_qdrant import Qdrant
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_vertexai.model_garden import ChatAnthropicVertex
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.services.tts import synthesize_text
from app.config import settings

project = "pacific-vault-426816-s6"
location = "us-east5"

model = ChatAnthropicVertex(
    model_name="claude-3-5-sonnet@20240620",
    project=project,
    location=location,
    max_tokens=250,
)
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")

system_prompt = (
    "You are an interviewer. You conducted an interview based on resume and job description. "
    "Use the following pieces of retrieved context to ask "
    "a question that can be answered with a short answer. "
    "Keep the question concise and to the point. "
    "ask about education, experience, skills, or other relevant information. "
    "Do not ask for multiple pieces of information in the same question. "
    "Do not ask questions on the same topic as after a follow-up question."
    "\n\n"

    "Job Description: {job_description}"

    "resume context: {context}"
)



contextualize_q_system_prompt = (
    "Given a chat history and the latest interviewee's response, "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history, but which is also relevant to the chat history. "
    "The question should be concise and to the point. "
)
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

async def handle_chat(chat):
    try:
        qdrant_db = Qdrant.from_existing_collection(
            embedding=embeddings,
            prefer_grpc=True,
            collection_name=f"resume_{chat.session_id}",
            url=settings.QDRANT_URL,
        )
        
        history_aware_retriever = create_history_aware_retriever(
            model, qdrant_db.as_retriever(), contextualize_q_prompt
        )
        
        qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

        qa_prompt = qa_prompt.format_messages(
            job_description=chat.job_description or "fullstack developer", 
        )
        print(qa_prompt)
        question_answer_chain = create_stuff_documents_chain(model, qa_prompt)

        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            lambda session_id: RedisChatMessageHistory(
                session_id, url=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"
            ),
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )
        config = {"configurable": {"session_id": chat.session_id}}
        response = conversational_rag_chain.invoke({"input": chat.message}, config=config)
        
        result = synthesize_text(response["answer"], "male")
        return {"result": result}
    except Exception as e:
        print(e)
        return {"error": str(e)}
