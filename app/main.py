import logging
import time
from app.config import Config
from app.database import init_db, get_db
from app.models.models import ArquivoMonitorado
from app.services.github_service import GitHubService
from app.services.llm_service import LLMService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_pipeline():
    init_db()
    db = get_db()
    
    gh_service = GitHubService(Config.GITHUB_TOKEN, Config.REPO_NAME)
    llm_service = LLMService(Config.GOOGLE_API_KEY)

    logger.info(f"Iniciando varredura no repo: {Config.REPO_NAME}")

    files = gh_service.get_repository_files()
    logger.info(f"Arquivos encontrados: {len(files)}")

    for github_file in files:
        db_file = db.query(ArquivoMonitorado).filter_by(file_path=github_file.path).first()
        
        # Só analisa se for novo ou se o SHA mudou
        if db_file and db_file.last_commit_sha == github_file.sha:
            logger.info(f"Skipping (sem mudanças): {github_file.path}")
            continue

        logger.info(f"Analisando: {github_file.path}...")
        
        content = github_file.decoded_content.decode('utf-8')
        result = llm_service.analyze(content, github_file.path)

        status = "CLEAN"
        
        if result.get('has_smell'):
            status = "ISSUES_FOUND"
            logger.warning(f"Smell detectado em {github_file.path}")
            issue_url = gh_service.create_issue(github_file.path, result)
            logger.info(f"Issue criada: {issue_url}")
        
        if not db_file:
            db_file = ArquivoMonitorado(file_path=github_file.path)
            db.add(db_file)
        
        db_file.last_commit_sha = github_file.sha
        db_file.status = status
        db_file.last_analyzed_at = datetime.now() 
        db.commit()
        
        time.sleep(4)

    logger.info("Pipeline finalizado com sucesso.")

if __name__ == "__main__":
    from datetime import datetime
    run_pipeline()