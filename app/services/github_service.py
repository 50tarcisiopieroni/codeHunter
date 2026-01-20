from github import Github, Repository, ContentFile
from typing import List, Optional

class GitHubService:
    def __init__(self, token: str, repo_name: str):
        self._client = Github(token)
        self._repo = self._client.get_repo(repo_name)
        
        self._ignored_extensions = {
            '.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', 
            '.pdf', '.zip', '.tar', '.gz', '.pyc', 
            '.lock', '.gitignore', '.env', '.md', '.txt'
        }

    def get_repository_files(self, extensions: Optional[List[str]] = None) -> List[ContentFile.ContentFile]:
        """
        Busca recursiva por arquivos.
        :param extensions: (Opcional) Lista de extensões permitidas ex: ['.py', '.js']. 
                            Se None, retorna todos exceto os ignorados.
        """
        files = []
        contents = self._repo.get_contents("")
        
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                if file_content.path not in ['node_modules', 'venv', '.git', '__pycache__']:
                    contents.extend(self._repo.get_contents(file_content.path))
            else:
                if self._should_process_file(file_content.name, extensions):
                    files.append(file_content)
        return files

    def _should_process_file(self, filename: str, allowed_extensions: List[str]) -> bool:
        """Regras para decidir se o arquivo deve ser analisado"""
        if allowed_extensions:
            return any(filename.endswith(ext) for ext in allowed_extensions)
            
        return not any(filename.endswith(ext) for ext in self._ignored_extensions)

    def create_issue(self, file_path: str, analysis_data: dict) -> str:
        title = f"[Code Smell] Detectado em {file_path}"
        body = (
            f"### Relatório Automático de Qualidade\n\n"
            f"**Arquivo:** `{file_path}`\n"
            f"**Tipo:** {analysis_data.get('smell_type', 'N/A')}\n"
            f"**Severidade:** {analysis_data.get('severity', 'N/A')}\n\n"
            f"#### Análise:\n{analysis_data.get('description', 'Sem descrição.')}\n\n"
            f"#### Sugestão de Correção:\n```\n{analysis_data.get('suggestion', '')}\n```"
        )
        issue = self._repo.create_issue(title=title, body=body)
        return issue.html_url