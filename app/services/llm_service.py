from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from models.ArquivosMonitorado import AnalysisResult

class LLMService:
    def __init__(self, api_key: str):
        self._llm = ChatGoogleGenerativeAI(
            model="models/gemma-3-27b-it",
            temperature=0,
            google_api_key=api_key
        )
        self._parser = JsonOutputParser(pydantic_object=AnalysisResult)

    def analyze(self, code: str, context: str) -> dict:
        prompt = PromptTemplate(
            template="""
            # Instrução
            Atue como um Arquiteto de Software senior. 
            Analise o seguinte arquivo de código: '{filename}'
            
            1. Identifique a linguagem de programação baseada na extensão ou sintaxe.
            2. Identifique as classes e métodos existentes
            3. Busque por violações de Clean Code, SOLID ou Code Smells comuns a essa linguagem.
            4. Se o código estiver limpo ou for um arquivo de configuração simples, retorne 'has_smell': false.

            # Instruções para output
            1.Todas as respostas devem ser na lingua portuguesa
            2.Caso haja mais que uma sugestão, deve ser enumerada e cada uma em uma linha
            
            # Código:
            {code}
            
            {format_instructions}
            """,
            input_variables=["code", "filename"],
            partial_variables={"format_instructions": self._parser.get_format_instructions()}
        )
        
        chain = prompt | self._llm | self._parser
        
        try:
            return chain.invoke({"code": code, "filename": context})
        except Exception as e:
            print(f"Erro na LLM: {e}")