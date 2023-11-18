from llama_index import VectorStoreIndex
from llama_index import Document
import multiprocessing
from dask import delayed, compute
from llama_index import download_loader
from pathlib import Path
PDFReader = download_loader("PDFReader")


class ChatBotManager:
    def __init__(self, rerank):
        self.rerank = rerank
        
    def get_docs(self, path):
        loader = PDFReader()
        document = loader.load_data(file=Path(path))
        return document
        
    def get_query_engine(self, document):
        
        # build index
        index = VectorStoreIndex.from_documents(documents=document)
        query_engine = index.as_query_engine(
            similarity_top_k=10, node_postprocessors=[self.rerank]
        )

        return query_engine
    
    # @staticmethod
    def chat_with_data_bot(self, prompt, query_engine):
        """
        Perform a chat interaction with the bot.
        
        Args:
            prompt: User's input.
            qa: Initialized RetrieverQueryEngine 
            
        Returns:
            Bot's response.
        """
        
        response = query_engine.query(
                        prompt,
                    )
        
        return  response
    
    def parallel_process_inputs(self, input_value, query_engine):
        if type(input_value) == str:
            results = self.chat_with_data_bot(input_value, query_engine)
        else: 
            with multiprocessing.Pool(processes=len(input_value)) as pool:
                # results = pool.starmap(self.chat_with_data_bot, [(input1, query_engine) for input1 in input_value])
                delayed_functions = [delayed(self.chat_with_data_bot)(input1, query_engine) for input1 in input_value]
                results = compute(*delayed_functions)
     
        return results