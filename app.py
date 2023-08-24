from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Produto 
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
produto_tag = Tag(name="Produto", description="Adição, visualização e remoção de previsões premium à base")
#comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um produtos cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi/swagger')


@app.post('/produto', tags=[produto_tag],
          responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_produto(form: ProdutoSchema):
    """Adiciona uma previsão premium à base de dados

    Retorna uma representação das previsões premium disponibilizadas no dia.
    """
    produto = Produto(
        nome=form.nome,
        quantidade=form.quantidade,
        valor=form.valor)
    logger.debug(f"Adicionada previsao de nome: '{produto.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(produto)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionada previsao de nome: '{produto.nome}'")
        return apresenta_produto(produto), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Previsão desta praia já adicionada já salvo na base :/"
        logger.warning(f"Erro ao adicionar previsão '{produto.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar previsão premium '{produto.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/produtos', tags=[produto_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
def get_produtos():
    """Faz a busca por todas as previsões premium cadastradas

    Retorna uma representação da listagem geral.
    """
    logger.debug(f"Coletando previsões ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produtos = session.query(Produto).all()

    if not produtos:
        # se não há produtos cadastrados
        return {"produtos": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(produtos))
        # retorna a representação de produto
        print(produtos)
        return apresenta_produtos(produtos), 200


@app.get('/produto', tags=[produto_tag],
         responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def get_produto(query: ProdutoBuscaSchema):
    """Faz a busca por uma previsão a partir do id da previsão

    Retorna uma representação das previsões premium do dia.
    """
    produto_nome = query.nome
    logger.debug(f"Coletando dados sobre produto #{produto_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produto = session.query(Produto).filter(Produto.id == produto_nome).first()

    if not produto:
        # se o produto não foi encontrado
        error_msg = "Previsão não encontrada na base :/"
        logger.warning(f"Erro ao buscar previsão '{produto_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Previsão encontrada: '{produto.nome}'")
        # retorna a representação de produto
        return apresenta_produto(produto), 200


@app.delete('/produto', tags=[produto_tag],
            responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def del_produto(query: ProdutoBuscaSchema):
    """Deleta uma previsão a partir do nome da praia informada.

    Retorna uma mensagem de confirmação da remoção.
    """
    produto_nome = unquote(unquote(query.nome))
    print(produto_nome)
    logger.debug(f"Deletando dados sobre a previsão #{produto_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Produto).filter(Produto.nome == produto_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado previsão #{produto_nome}")
        return {"mesage": "Previsão removida", "id": produto_nome}
    else:
        # se o produto não foi encontrado
        error_msg = "Previsão não encontrada na base :/"
        logger.warning(f"Erro ao deletar produto #'{produto_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


