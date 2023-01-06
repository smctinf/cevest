from django.urls import path
from . import views

urlpatterns = [
    #Administrativo
    path('sair', views.sair, name='sair'),

    # Tem esse "alocados" aqui que aparentemente foi usado apenas para teste. Levantar se ele realmente é necessário
    # Essa view está fazendo uma consulta no curso de id = 2 e está retornando uma consula (select), n está sendo usada por nenhuma
    # outra rota e não tem referência no html
    # path('alocados', views.alocados, name='alocados'),

    # Esse aqui lista todos os alunos portadores de necessidades especiais, a tabela é um pouco simples demais e exibe apenas
    # o nome e o id do aluno. Levantar a possibilidade de criar uma página de visualização para cad aluno (estilo sistema de cursos livres)
    path('portador', views.portador, name='portador'),

    # TURMAS

    # Pelo o que eu entendi esse confirmar tudo não faz nada, pelo menos a view n está recebendo nenhum dado no POST, precisa
    # de maior investigação
    path('turmas/confirmar', views.confirmar_turma, name='confirmar_turma'),
    # Tem uma regra para a exibição de somente algumas turmas, e com os dados atuais do cevest não está sendo
    # exibida nenhuma turma
    path('turmas/listar',views.listar_turmas, name = "listar_turmas"),
    # Ele busca todas as turmas previstas com o id de curso informado, mas no momento tbm n há nenhuma turma prevista que
    # se encaixa nas regras do filter da view
    path('turma_prevista/<int:idcurso>', views.turma_prevista, name='turma_prevista'),


    # A página do recibo recebe o id do aluno e redireciona para o recibo_ind/<int:pk>
    path('recibo_ind', views.recibo_ind, name='recibo_individual'),
    # Essa rota cria um mini recibo com as informações do aluno, precisa de refatoração
    path('recibo_ind/<int:pk>', views.recibo_ind2, name='recibo_individual2'),
    
    # Essa pauta aqui é bonitinha. Você escolhe a turma que você quer e redireciona para pauta2/<id>
    path('pauta', views.pauta, name='pauta'),
    # A pauta criada tem todos os alunos, a frequência... só tem um pequeno erro que a primeira página do pdf gerado vem em branco
    path('pauta2/<int:turma_id>', views.pauta2, name='pauta2'),

    #Usuário
    path('', views.index, name='index'),
    # Esse retorna todos os cursos de determinado programa (no caso, o <id> é o id do programa). Acho que não precisa mexer nesse
    # aqui nem tão cedo. Tá bem bonitinho
    path('cursos/<int:pk>', views.cursos, name='cursos'),
    # Esse aqui retorna a descrição do curso, carga horária e idade mínima do curso com id informado.
    # Mas a página tá precisando de refatoração
    path('curso/<int:pk>', views.curso, name='curso'),
    # Esse aqui é meio estranho, vc informa o id e ele retorna o cpf e data de nascimento para ser alterado?
    # Não entendi muito bem como funciona. De qualquer forma é uma falha de segurança, pq vc pode informar um id e receber de
    # cara o cpf e data de nascimento da pessoa
    path('altera/<int:pk>', views.altera, name='altera'),
    # Essa rota aqui usa um request.session, nem sabia que o django tinha essa propriedade. Eu assumo que
    # é um cookie de sessão que é atribuido ao aluno, só n sei quando...
    path('altera_cadastro',views.AlterarCadastro, name='altera_cadastro'),
    # Outra daquelas páginas com o altera_cpf, n sei se funciona
    path('detalhe', views.detalhe, name='detalhe'),
    # Mostra todas as matrizes de um determinado curso. As matrizes são as "diciplinas" de cada curso
    path('matriz/<int:idcurso>', views.matriz, name='matriz'),

    # bem auto explicativo esse kkkkkkkk, mas seria interessante jogar esse aqui para uma rota específica para uma api interna
    path('get_bairro/<int:cidade_id>', views.get_bairro, name='get_bairro'),
    # Uma telinha antes de ir para a rota "lista_alocados", tem uma explicação de como os alunos são selecionados pelo sistema
    path('resultado', views.resultado, name='resultado'),
    # Tem alguma lógica sendo executada na função getListaAlocados() mas aparentemente não há nenhum dado para ser coletado
    # ou possível algum erro, precisa de maior investigação
    path('lista_alocados',views.lista_alocados, name = "lista_alocados"),
    # Tabelas com indicadores. Abre surpreendentemente rápido. Mas precisa de gráficos!
    path('indicadores',views.indicadores, name = "indicadores"),

    # já comentei sobre essa rota. Meio mistério ainda se elas funcionam ou não, precisa de mais investigação
    path('altera_cpf', views.altera_cpf, name='altera_cpf'),
    # O nome é meio ruim, ele na realidade é a *pré-matricula*
    path('cadastro', views.cadastro, name='cadastro'),



    path('ajax/load_bairros/', views.load_bairros, name = 'ajax_load_bairros'),
]