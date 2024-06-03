from sqlalchemy import Column, Integer, String, ForeignKey,func , create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Criar as tabelas
Base = declarative_base()

class Fornecedor(Base):
    __tablename__ = 'fornecedores'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    telefone = Column(String(20))
    email = Column(String(50))
    endereco = Column(String(100))

class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(200))
    preco = Column(Integer)
    fornecedor_id = Column(Integer, ForeignKey('fornecedores.id'))

# Estabelece a relação entre Produto e Fornecedor
fornecedor = relationship("Fornecedor")

# Criar engine
engine = create_engine('sqlite:///bancodesafio.db', echo=True)
print("Conexão com SQLite estabelecida.")

# Criar as tabelas no banco de dados
Base.metadata.create_all(engine)

# Criar uma classe de sessão configurada
Session = sessionmaker(bind=engine)

# Criar uma sessão
session = Session()

resultado = session.query(
    Fornecedor.nome,
    func.sum(Produto.preco).label('total_preco')
).join(Produto, Fornecedor.id == Produto.fornecedor_id
).group_by(Fornecedor.nome).all()

for nome, total_preco in resultado:
    print(f"Fornecedor: {nome}, Total Preço: {total_preco}")