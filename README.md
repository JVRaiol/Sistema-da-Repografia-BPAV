Documentação do Sistema de Cálculo de Renda para Reprografia

1. Visão Geral

O sistema foi desenvolvido para calcular a renda gerada por serviços de reprografia da Biblioteca Pública Arthur Vianna, incluindo cópias, impressões e digitalizações. Ele permite inserir os valores dos serviços realizados e obter uma estimativa de renda, além de salvar e atualizar esses dados.

2. Funcionalidades

2.1. Calculadora Rápida

Permite o cálculo rápido da renda baseada nos valores inseridos.

Utiliza os seguintes percentuais de lucro:

Cópias: 20%

Impressões: 20%

Digitalizações: 50%

Exibe os valores calculados na tela.

2.2. Salvamento e Atualização de Valores

Os valores de serviços realizados são armazenados num diretório no disco C arquivo e salvos no arquivo dados.txt.

Caso o arquivo não exista, ele é criado automaticamente.

A função de atualização permite modificar os valores e salvar as alterações.

2.3. Geração de Relatório

O Sistema é capaz de gerar um relatório diário e detalhado de todos os serviços realizados na repografia para avaliação da coordenação


2.3. Interface Gráfica

Desenvolvida com Tkinter, apresenta campos de entrada e botões para interação.

Inclui um ícone personalizado e exibição de mensagens para o usuário.

3. Estrutura do Arquivo dados.txt

O arquivo dados.txt armazena quatro valores, separados por linhas:

Quantidade de cópias realizadas

Quantidade de impressões realizadas

Quantidade de digitalizações realizadas

Total de serviços executados

Se o arquivo não existir, o sistema inicializa os valores como 0.0.

4. Principais Funções

calculadora_rapida()

Obtém os valores inseridos pelo usuário nos campos de entrada.

Calcula a renda gerada por cópias, impressões e digitalizações.

Exibe os resultados na tela.

salvar_novos_valores()

Obtém os novos valores digitados pelo usuário.

Atualiza e salva os valores no arquivo dados.txt.

Fecha a janela de edição dos valores.

carregar_dados()

Lê os valores do arquivo dados.txt, garantindo que tenham um formato válido.

Se o arquivo estiver ausente, cria um novo com valores padrão 0.0.

5. Requisitos

Python 3

Biblioteca Tkinter (padrão no Python)

Biblioteca reportlab

Biblioteca PIL

Biblioteca OS

Biblioteca openpyxls

Biblioteca Datetime

Diretório Sistem no Disco C


6. Melhorias Futuras

Implementação de um banco de dados para armazenar histórico de serviços.

Inclusão de relatórios detalhados sobre a renda mensal.

Melhorias na interface para facilitar a usabilidade.


