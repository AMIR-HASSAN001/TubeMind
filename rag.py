from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda,
)
from langchain_core.output_parsers import StrOutputParser

from config import GROQ_API_KEY


# ----------------------------------------
# Embedding Model
# ----------------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

# ----------------------------------------
# LLM
# ----------------------------------------

llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0,
)

# ----------------------------------------
# Prompt
# ----------------------------------------

prompt = ChatPromptTemplate.from_template("""
You are an AI assistant that answers questions about a YouTube video.

Use ONLY the provided transcript.

Do not exaggerate or add information that is not present in the transcript.

If the transcript does not contain the answer, reply:

"I couldn't find that information in the transcript."

Context:
{context}

Question:
{question}

Answer:
""")


# ----------------------------------------
# Split Transcript
# ----------------------------------------

def split_transcript(transcript):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=150,
    )

    return splitter.create_documents([transcript])


# ----------------------------------------
# Format Retrieved Documents
# ----------------------------------------

def format_docs(docs):

    return "\n\n".join(
        doc.page_content
        for doc in docs
    )


# ----------------------------------------
# Build RAG Chain
# ----------------------------------------

# ----------------------------------------
# Build RAG Chain
# ----------------------------------------

def create_chain(transcript):

    documents = split_transcript(transcript)

    

    vector_store = FAISS.from_documents(
        documents,
        embeddings,
    )

    retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 8,
        "fetch_k": 20,
        "lambda_mult": 0.5
    }
)
    

    # Debug: Show retrieved documents
    def debug_docs(docs):

        print("\n" + "=" * 60)
        print("Retrieved Documents")
        print("=" * 60)

        for i, doc in enumerate(docs, 1):
            print(f"\nDocument {i}\n")
            print(doc.page_content[:500])

        return format_docs(docs)

    # Debug: Show final prompt
    def debug_prompt(data):

        prompt_value = prompt.invoke(data)

        print("\n" + "=" * 80)
        print("FINAL PROMPT SENT TO GROQ")
        print("=" * 80)
        print(prompt_value)
        print("=" * 80 + "\n")

        return prompt_value

    chain = (
    RunnableParallel(
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
    )
    | prompt
    | llm
    | StrOutputParser()
)

    return chain