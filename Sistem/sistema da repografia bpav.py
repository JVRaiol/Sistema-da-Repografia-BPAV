import tkinter as tk
from tkinter import messagebox
from openpyxl import load_workbook
from openpyxl.styles import Protection
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.pagesizes import letter, landscape
from PIL import Image, ImageTk
import os


def atualizar_valores_iniciais():
    try:
        with open("C://Sistem/dados.txt", "r") as dados:
             lista = [x.strip() for x in dados]
        v1, v2, v3, v4 = float(lista[0]), float(lista[1]), float(lista[2]), float(lista[3])

        # Atualiza o resultado dos valores iniciais na interface
        label_resultado_inic.config(text=f"VALORES INICIAIS\n\nCópias: {int(v1)}\nImp. Kyocera: {int(v2)}\nImp. Brother: {int(v3)}\nDigitalização: {int(v4)}")
        window.after(500, atualizar_valores_iniciais)  # Atualiza a cada 500 milissegundos (meio segundo)
    
    except Exception as e:
        label_resultado_inic.config(text="Erro ao calcular os resultados.")
        window.after(500, atualizar_resultado)


# Função que será chamada para calcular e atualizar os resultados financeiros em tempo real
def atualizar_resultado():
    try:
        # Lê os valores dos campos
        c = float(entry_copias.get()) if entry_copias.get() else 0.0
        ik = float(entry_imp_koycera.get()) if entry_imp_koycera.get() else 0.0
        ib = float(entry_imp_brother.get()) if entry_imp_brother.get() else 0.0
        s = float(entry_scaners.get()) if entry_scaners.get() else 0.0
        pc = float(entry_perdidas_c.get()) if entry_perdidas_c.get() else 0.0
        pik = float(entry_perdidas_ik.get()) if entry_perdidas_ik.get() else 0.0
        pib = float(entry_perdidas_ib.get()) if entry_perdidas_ib.get() else 0.0
        p2 = float(entry_perdS.get()) if entry_perdS.get() else 0.0
        pix = float(entry_pix.get()) if entry_pix.get() else 0.0

        data_atual = datetime.now().strftime("%d/%m/%Y")

        registro_pix = text_registpix.get("1.0", "end-1c").strip()
        obs = text_obs.get("1.0", "end-1c").strip()


		# Lê os valores registrados em dados.txt para realizar as subtrações
        with open("C://Sistem/dados.txt", "r") as dados:
            lista = [x.strip() for x in dados]
		
        # Lê os valores do arquivo para subtração
        v1, v2, v3, v4 = float(lista[0]), float(lista[1]), float(lista[2]), float(lista[3])

        # Calcula as subtrações
        x = ik - v2
        y = ib - v3
        z = c - v1
        k = s - v4

        # Calcula as rendas parciais
        rik = x * 0.2
        rib = y * 0.2
        rc = z * 0.2
        rs = k * 0.5
        ri = rik + rib

        # Calcula o valor final da renda
        p1 = pc + pib + pik
        ps = p2 * 0.5
        perd = p1 * 0.2 + ps
        vpf = (ri + rc + rs) - perd
        ve = vpf - pix
        rend_tot = pix + ve

        if ve < 0:
             ve = 0
        if rend_tot < 0:
             rend_tot = 0

        # Atualiza o resultado financeiro na interface
        label_resultado_financ.config(text=f"Renda em Espécie: R${ve:.2f}\nRenda em pix: R${pix:.2f}\nRenda Total: R${rend_tot:.2f}")
        window.after(500, atualizar_resultado) #Atualiza a cada 500 milissegundos (meio segundo)
        
    except Exception as e:
        label_resultado_financ.config(text="Erro ao calcular os resultados.")
        window.after(500, atualizar_resultado)

#função que atualiza a relação de páginas no painel e dar o valor de acordo com as páginas
def atualizar_relacao_paginas():
     try:
        
        with open("C://Sistem/dados.txt", "r") as dados:
            lista = [x.strip() for x in dados]
		
        # Lê os valores do arquivo para subtração
        v1, v2, v3, v4 = float(lista[0]), float(lista[1]), float(lista[2]), float(lista[3])

        #valores das páginas
        c = float(entry_copias.get()) if entry_copias.get() else 0.0
        ik = float(entry_imp_koycera.get()) if entry_imp_koycera.get() else 0.0
        ib = float(entry_imp_brother.get()) if entry_imp_brother.get() else 0.0
        s = float(entry_scaners.get()) if entry_scaners.get() else 0.0 

        #valores das perdidas
        pc = float(entry_perdidas_c.get()) if entry_perdidas_c.get() else 0.0
        pik = float(entry_perdidas_ik.get()) if entry_perdidas_ik.get() else 0.0
        pib = float(entry_perdidas_ib.get()) if entry_perdidas_ib.get() else 0.0
        p2 = float(entry_perdS.get()) if entry_perdS.get() else 0.0
        pix = float(entry_pix.get()) if entry_pix.get() else 0.0

        rel_cop = c - v1
        rel_ik = ik - v2
        rel_ib = ib - v3
        rel_dig = s - v4

        #atualiza a relação de páginas no painel (na label)
        label_relacao_paginas.config(text=f"RELAÇÃO DE PÁGINAS DO DIA \n\n Cópias Kyocera: {int((rel_cop) - pc)}       R${int(((rel_cop) - pc))*0.2:.2f}\n Impressões Kyocera: {int((rel_ik) - pik)}     R${(int(rel_ik) - pik)*0.2:.2f}\n Impressões Brother: {int((rel_ib) - pib)}    R${(int(rel_ib) - pib)*0.2:.2f}\n Digitalização Kyocera: {int((rel_dig) - p2)}    R${(int(rel_dig) - p2)*0.5:.2f}")
        window.after(500, atualizar_relacao_paginas) #atualiza em cada 500 milissegundos (meio segundo)
             
     except Exception as e:
        label_relacao_paginas.config(text="Erro ao calcular os resultados.")
        window.after(500, atualizar_relacao_paginas)         

# Função para o cálculo final ao clicar no botão
def calcular_renda():
    try:
        # Lê os dados do arquivo
        with open("C://Sistem/dados.txt", "r") as dados:
            lista = [x.strip() for x in dados]
        
        ac, aik, aib, asc = float(lista[0]), float(lista[1]), float(lista[2]), float(lista[3])
        
        # Obtém os valores das entradas (interface gráfica)
        c = float(entry_copias.get()) if entry_copias.get() else ac
        ik = float(entry_imp_koycera.get()) if entry_imp_koycera.get() else aik
        ib = float(entry_imp_brother.get()) if entry_imp_brother.get() else aib
        s = float(entry_scaners.get()) if entry_scaners.get() else asc
        pc = float(entry_perdidas_c.get()) if entry_perdidas_c.get() else 0.0
        pik = float(entry_perdidas_ik.get()) if entry_perdidas_ik.get() else 0.0
        pib = float(entry_perdidas_ib.get()) if entry_perdidas_ib.get() else 0.0
        p2 = float(entry_perdS.get()) if entry_perdS.get() else 0.0
        pix = float(entry_pix.get()) if entry_pix.get() else 0.0

        # Data atual
        data_atual = datetime.now().strftime("%d/%m/%Y")
        
        # Lê os registros de texto
        registro_pix = text_registpix.get("1.0", "end-1c").strip()
        obs = text_obs.get("1.0", "end-1c").strip()
        
        # Lê novamente os valores do arquivo para subtrações
        with open("C://Sistem/dados.txt", "r") as dados:
            lista = [x.strip() for x in dados]
        
        # Extrai os valores de dados.txt
        v1, v2, v3, v4 = float(lista[0]), float(lista[1]), float(lista[2]), float(lista[3])

        # Realiza as subtrações
        x = ik - v2
        y = ib - v3
        z = c - v1
        k = s - v4

        # Calcula as rendas parciais
        rik = x * 0.2
        rib = y * 0.2
        rc = z * 0.2
        rs = k * 0.5
        ri = rik + rib

        # Calcula o valor final da renda
        p1 = pc + pik + pib
        ps = p2 * 0.5
        perd = p1 * 0.2 + ps
        vpf = (ri + rc + rs) - perd
        ve = vpf - pix
        rend_tot = pix + ve


        # Exibe o resultado
        messagebox.showinfo("Resultado", "Cálculo finalizado! Valores salvos no Banco de dados.")
    
        # Atualiza os dados no arquivo
        with open("C://Sistem/dados.txt", "w") as dados:
            dados.write(f"{c}\n{ik}\n{ib}\n{s}")
        
        # Gerar o PDF com os dados calculados
        gerar_pdf(c, ik, ib, s, p1, p2, pix, ve, rend_tot, registro_pix, obs, data_atual, v1, v2, v3, v4, x, y, z, k, rik, rib, rc, rs, pc, pik, pib, ps)
    
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

        
# Função para gerar o PDF do relatório
def gerar_pdf(c, ik, ib, s, p1, p2, pix, ve, rend_tot, registro_pix, obs, data_atual, v1, v2, v3, v4, x, y, z, k, rik, rib, rc, rs, pc, pik, pib, ps):
    try:
        nome_arquivo_pdf = "relatorio.pdf"
         # Obtém o caminho da área de trabalho do usuário
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        nome_arquivo_pdf = os.path.join(desktop_path, "relatorio.pdf")
        
        # Aumentando as margens para garantir que o título caiba
        doc = SimpleDocTemplate(nome_arquivo_pdf, pagesize=letter, 
                                rightMargin=30, leftMargin=30, topMargin=100, bottomMargin=50)

        # Definindo os estilos
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        normal_style = styles['Normal']

        # Estilo personalizado para o título
        header_style = ParagraphStyle(name="Header", fontSize=16, fontName="Helvetica-Bold", textColor=colors.black, 
                                      alignment=1, spaceAfter=20)

        # Estilo da tabela
        table_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                                  ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                  ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                  ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                  ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                  ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                  ('SIZE', (0, 0), (-1, -1), 12)])

        # Estilo para itens da tabela
        item_style = ParagraphStyle(name="Item", fontSize=12, fontName="Helvetica", spaceAfter=8)

        # Dados para a tabela principal
        dados = [
            ["produto", "Valor inicial", "valor final", "páginas do dia", "perdidas", "pago" ],
            ["Cópias",    f"{int(v1)}",   f"{int(c)}", f"{int(c-v1)}",  f"{int(pc)}", f"R${rc -(pc*0.2):.2f} ({int((c-v1) - pc)} páginas)"],
            ["Impressões Kyocera", f"{int(v2)}", f"{int(ik)}", f"{int(ik-v2)}", f"{int(pik)}", f"R${rik - (pik*0.2):.2f} ({int((ik-v2) - pik)} páginas)"],
            ["Impressões Brother", f"{int(v3)}", f"{int (ib)}", f"{int(ib-v3)}", f"{int(pib)}", f"R${rib- (pib*0.2):.2f} ({int((ib-v3) - pib)} páginas)"],
            ["Digitalização", f"{int(v4)}", f"{int(s)}", f"{int(s-v4)}", f"{int(p2)}", f"R${rs-p2:.2f} ({int((s-v4) - p2)} páginas)"],
        ]

        # Dados para a nova tabela (adicionada)
        dados_nova_tabela = [
            ["Financeiro", "Valor"],
            ["Renda em espécie", f"R${ve:.2f}"],
            ["Renda em Pix", f"R${pix:.2f}"],
            ["RENDA TOTAL", f"R${rend_tot:.2f}" ],
        ]
        
        
        # Elementos do PDF
        elementos = []

        # Adicionar a logo no topo do PDF
        logo_path = "C://Sistem/logo.png"
        elementos.append(Spacer(1, 10))  # Espaço entre o topo e a logo

        # Cabeçalho com o nome do relatório
        titulo = Paragraph(f"Relatório Repografia - {data_atual}", header_style)
        elementos.append(titulo)

        # Espaço entre o título e a tabela principal
        elementos.append(Spacer(1, 30))  # Espaço entre o título e a tabela principal

        # Função para desenhar a logo no topo da página
        def add_logo(canvas, doc):
            try:
                logo_width = 100  # Largura da logo
                page_width = 612  # Largura da página (tamanho letter)
                x_position = (page_width - logo_width) / 2  # Calcula a posição X para centralizar a logo
                canvas.drawImage(logo_path, x_position, 730, width=logo_width, height=50)  # Ajuste o tamanho da logo conforme necessário
            except Exception as e:
                print(f"Erro ao adicionar logo: {e}")

        # Adicionando a tabela de dados (tabela principal)
        tabela = Table(dados, colWidths=[130, 80, 80, 95, 52, 120])
        tabela.setStyle(table_style)
        elementos.append(tabela)

        # Adicionando a nova tabela
        elementos.append(Spacer(1, 60))  # Espaço entre as tabelas
        tabela_nova = Table(dados_nova_tabela, colWidths=[180, 80, 100, 80])
        tabela_nova.setStyle(table_style)
        elementos.append(tabela_nova)

        # Espaço antes das observações
        elementos.append(Spacer(1, 50))

        # Registro Pix e Observações
        elementos.append(Paragraph(f"<b>Registros de pix:</b> {registro_pix}", item_style))
        elementos.append(Spacer(1, 30)) # Espaço antes das observações
        
        elementos.append(Paragraph(f"<b>Observações:</b> {obs}", item_style))

        # Adicionando um rodapé
        rodape = Paragraph("<font size=8>Gerado por Sistema da Xerox</font>", normal_style)
        elementos.append(Spacer(1, 40))  # Espaço antes do rodapé
        elementos.append(rodape)

        # Gerar o PDF com a função add_logo para adicionar a logo
        doc.build(elementos, onFirstPage=add_logo, onLaterPages=add_logo)

        messagebox.showinfo("Sucesso", "Relatório gerado com sucesso!\nDisponível na área de trabalho")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro ao gerar o PDF: {e}")

def calculadora_rapida():
    try:
        # definir variaveis
        c = float(calculadora_c.get()) if calculadora_c.get() else 0.0
        imp = float(calculadora_imp.get()) if calculadora_imp.get() else 0.0
        dig = float(calculadora_digit.get()) if calculadora_digit.get() else 0.0

        rend_c = c * 0.2
        rend_imp = imp * 0.2
        rend_dig = dig * 0.5

        tot = rend_c + rend_imp + rend_dig
        
        label_resultado_calc.config(text=f"Valor a cobrar: R${tot:.2f}")
        window.after(500, calculadora_rapida) #atualiza em cada 500 milissegundos (meio segundo)
    except Exception as e:
        label_resultado_calc.config(text=f"Ocorreu um erro na calculadora: {e}")
        window.after(500, calculadora_rapida) #atualiza em cada 500 milissegundos (meio segundo)     

# Função para mostrar a janela de alerta
def mostrar_alerta():
    janela_alerta = tk.Toplevel(window)
    janela_alerta.title("Atenção!")
    janela_alerta.iconbitmap('c:/sistem/logo.ico')
    janela_alerta.geometry("500x200")
    janela_alerta.configure(bg="white")
    janela_alerta.transient(window)
    janela_alerta.grab_set()
    janela_alerta.focus_force()
    msg_alerta = "Atenção: Por favor, insira os valores corretamente. Valores incorretos podem comprometer o funcionamento do programa inteiro!"
    label_alerta = tk.Label(janela_alerta, text=msg_alerta, bg="white", font=("Arial", 12, "bold"), wraplength=400)
    label_alerta.pack(pady=20)
    btn_fechar = tk.Button(janela_alerta, text="Fechar", command=janela_alerta.destroy, bg="red")
    btn_fechar.pack(pady=10)
    janela_alerta.wait_window()
    

# Função para abrir a janela de redefinir valores
def janela_definir_novos_valores():
    global entry_novo_valor_copias, entry_novo_valor_imp_kyocera, entry_novo_valor_imp_brother, entry_novo_valor_scaners
    
    global janela_novos_valores
    janela_novos_valores = tk.Toplevel(window)
    janela_novos_valores.title("Definir Novos Valores iniciais")
    janela_novos_valores.geometry("400x400")
    janela_novos_valores.configure(bg="lightcoral")
    janela_novos_valores.iconbitmap('C:/sistem/logo.ico')
	
    # Labels e entradas para redefinir os valores
    tk.Label(janela_novos_valores, text="Novo valor para Cópias:", font=("Arial", 12)).pack(pady=10)
    entry_novo_valor_copias = tk.Entry(janela_novos_valores, font=("Arial", 12), relief="groove", borderwidth=2)
    entry_novo_valor_copias.pack(pady=5)
    
    tk.Label(janela_novos_valores, text="Novo valor para Impressões Kyocera:", font=("Arial", 12)).pack(pady=10)
    entry_novo_valor_imp_kyocera = tk.Entry(janela_novos_valores, font=("Arial", 12), relief="groove", borderwidth=2)
    entry_novo_valor_imp_kyocera.pack(pady=5)

    tk.Label(janela_novos_valores, text="Novo valor para Impressões Brother:", font=("Arial", 12)).pack(pady=10)
    entry_novo_valor_imp_brother = tk.Entry(janela_novos_valores, font=("Arial", 12), relief="groove", borderwidth=2)
    entry_novo_valor_imp_brother.pack(pady=5)

    tk.Label(janela_novos_valores, text="Novo valor para Digitalização:", font=("Arial", 12)).pack(pady=10)
    entry_novo_valor_scaners = tk.Entry(janela_novos_valores, font=("Arial", 12), relief="groove", borderwidth=2)
    entry_novo_valor_scaners.pack(pady=5)    

    # Botão para salvar os novos valores
    btn_salvar_novos_valores = tk.Button(janela_novos_valores, text="Salvar Novos Valores", command=salvar_novos_valores, bg="lightgreen", font=("Arial", 12, "bold"))
    btn_salvar_novos_valores.pack(pady=20)  

#funcao para salvar os novos valores
def salvar_novos_valores():
	try:
		# Abrir o arquivo para ler os valores atuais
		with open("C://Sistem/dados.txt", "r") as dados:
			lista = [x.strip() for x in dados]
            
		# Atribuindo os valores atuais do arquivo às variáveis
		nc, nik, nib, ns = float(lista[0]), float(lista[1]), float(lista[2]), float(lista[3])

		# Pegar os valores inseridos pelo usuário nos campos de entrada
		novo_valor_copias = entry_novo_valor_copias.get()
		novo_valor_imp_kyocera = entry_novo_valor_imp_kyocera.get() 
		novo_valor_imp_brother = entry_novo_valor_imp_brother.get() 
		novo_valor_scaners = entry_novo_valor_scaners.get()

		# condicao se os campos de entrada de valores estiverem vazios
		novo_valor_copias = novo_valor_copias if novo_valor_copias not in ('') else str(nc)
		novo_valor_imp_kyocera = novo_valor_imp_kyocera if novo_valor_imp_kyocera not in ('') else str(nik)
		novo_valor_imp_brother = novo_valor_imp_brother if novo_valor_imp_brother not in ('') else str(nib)
		novo_valor_scaners = novo_valor_scaners if novo_valor_scaners not in ('') else str(ns)

		# Grava os novos valores no banco de dados
		with open(r"C:\Sistem\dados.txt", "w") as dados:
			dados.write(f"{novo_valor_copias}\n{novo_valor_imp_kyocera}\n{novo_valor_imp_brother}\n{novo_valor_scaners}")

		# Mensagem de sucesso e fechamento da janela
		messagebox.showinfo("Sucesso", "Novos valores definidos com sucesso!")
		janela_novos_valores.destroy()  # Fecha a janela de redefinir valores
		
	except Exception as e:
		# Caso ocorra um erro, exibe uma mensagem de erro
		messagebox.showerror("Erro", f"Ocorreu um erro ao salvar os novos valores: {e}")

#decrição sobre o programa
def sobre():
     global janela_sobre
     janela_sobre = tk.Toplevel(window)
     janela_sobre.title("Sobre o programa")
     janela_sobre.geometry("400x400")
     janela_sobre.iconbitmap("C://sistem/logo.ico")
     janela_sobre.configure(bg="lightyellow")
     
     texto_sobre = (
        "O Sistema da Repografia BPAV foi desenvolvido por João Victor Raiol, estagiário da CBPAV, destinado a calcular e controlar a "
        "renda e serviços de reprografia da Biblioteca Pública Arthur Vianna, "
        "incluindo cópias, impressões e digitalizações.\n\n"
        "O sistema foi criado para uso exclusivo da instituição e não pode ser "
        "replicado para outras finalidades.\n\n"
        "Para mais informações, entre em contato com o desenvolvedor\n"
        "Dev.jvraiol@gmail.com \n"
        "(91)98253-6155"
    )
    
     label_sobre = tk.Label(janela_sobre, text=texto_sobre, font=("Arial", 16) , bg="lightyellow", justify="left", wraplength=380) #wraplength serve para quebrar a linha quando o texto chega numa determinada largura
     label_sobre.pack(pady=5)                                                                                                      #nesse caso, 380 pixels

# Janela principal
window = tk.Tk()
window.title("Sistema da Repografia CBPAV")
window.geometry("1280x650+0+0") #0+0 serve para definir a posição da janela na tela (linha 0 coluna 0)
window.configure(bg="white")
font_padrao = ("Arial", 12)
window.iconbitmap('c:/sistem/logo.ico')

# Carregar a imagem do topo
top_image = Image.open("c:/sistem/logoazul.jpeg")
top_image = top_image.resize((200, 100), Image.LANCZOS)
top_photo = ImageTk.PhotoImage(top_image)

# Criar um label para exibir a imagem do topo
top_label = tk.Label(window, image=top_photo, bg="beige")
top_label.grid(row=0, column=0, columnspan=4, pady=(20, 19))

# Exibe a mensagem de alerta ao iniciar
mostrar_alerta()

# Layout e entradas da interface principal
tk.Label(window, text="Cópias Kyocera:", bg="light blue", font=font_padrao).grid(row=1, column=0, sticky="e", padx=2, pady=5)
entry_copias = tk.Entry(window, font=font_padrao, bg="light gray")
entry_copias.grid(row=1, column=1, padx=3, pady=5, sticky="w")
tk.Label(window, text="Perdidas Cópias:", bg="light blue", font=font_padrao).grid(row=1, column=2, sticky="e", padx=2, pady=5)
entry_perdidas_c = tk.Entry(window, font=font_padrao, bg="light gray")
entry_perdidas_c.grid(row=1, column=3, padx=3, pady=5, sticky="w")

tk.Label(window, text="Impressões Kyocera:", bg="light blue", font=font_padrao).grid(row=2, column=0, sticky="e", padx=2, pady=5)
entry_imp_koycera = tk.Entry(window, font=font_padrao, bg="light gray")
entry_imp_koycera.grid(row=2, column=1, padx=3, pady=5, sticky="w")
tk.Label(window, text="Perdidas Imp. Kyocera:", bg="light blue", font=font_padrao).grid(row=2, column=2, sticky="e", padx=2, pady=5)
entry_perdidas_ik = tk.Entry(window, font=font_padrao, bg="light gray")
entry_perdidas_ik.grid(row=2, column=3, padx=3, pady=5, sticky="w")

tk.Label(window, text="Impressões Brother:", bg="lightblue", font=font_padrao).grid(row=3, column=0, sticky="e", padx=2, pady=5)
entry_imp_brother = tk.Entry(window, font=font_padrao, bg="light gray")
entry_imp_brother.grid(row=3, column=1, padx=3, pady=5, sticky="w")
tk.Label(window, text="Perdidas Imp. Brother:", bg="lightblue", font=font_padrao).grid(row=3, column=2, sticky="e", padx=2, pady=5)
entry_perdidas_ib = tk.Entry(window, font=font_padrao, bg="light gray")
entry_perdidas_ib.grid(row=3, column=3, padx=3, pady=5, sticky="w")

tk.Label(window, text="Digitalização Kyocera:", bg="light blue", font=font_padrao).grid(row=4, column=0, sticky="e", padx=2, pady=5)
entry_scaners = tk.Entry(window, font=font_padrao, bg="light gray")
entry_scaners.grid(row=4, column=1, padx=3, pady=5, sticky="w")
tk.Label(window, text="Perdidas Digitalização:", bg="light blue", font=font_padrao).grid(row=4, column=2, sticky="e", padx=2, pady=5)
entry_perdS = tk.Entry(window, font=font_padrao, bg="light gray")
entry_perdS.grid(row=4, column=3, padx=3, pady=5, sticky="w")

tk.Label(window, text="Receita em Pix:", bg="lightblue", font=font_padrao).grid(row=5, column=0, sticky="e", padx=2, pady=5)
entry_pix = tk.Entry(window, font=font_padrao, bg="light gray")
entry_pix.grid(row=5, column=1, padx=3, pady=5, sticky="w")

# Caixa de texto para "Observações" e "Registro Pix"
tk.Label(window, text="Observações:", bg="light blue", font=font_padrao).grid(row=6, column=0, sticky="e", padx=2, pady=5)
text_obs = tk.Text(window, height=5, width=40, font=font_padrao, bg="light gray")
text_obs.grid(row=6, column=1, padx=3, pady=5)
tk.Label(window, text="Registro Pix:", bg="light blue", font=font_padrao).grid(row=7, column=0, sticky="e", padx=2, pady=5)
text_registpix = tk.Text(window, height=5, width=40, font=font_padrao, bg="light gray")
text_registpix.grid(row=7, column=1, padx=1, pady=1)

# Label para exibir o resultado financeiro em tempo real
label_resultado_financ = tk.Label(window, text="Renda Total", font=("Arial", 14, "bold"), fg="blue", bg="light blue", bd=2, relief="solid")
label_resultado_financ.grid(row=6, column=2, columnspan=2, padx=8, pady=5)

# Label para exibir o resultado de valores iniciais em tempo real
label_resultado_inic = tk.Label(window, text="Valores Iniciais" , font=("Arial", 14, "bold"), fg="blue", bg="light blue", bd=2, relief="solid")
label_resultado_inic.grid(row=7, column=2, columnspan=2, padx=8, pady=5)

#Label para exibir a relacao de paginas em tempo real
label_relacao_paginas = tk.Label(window, text="Relação de páginas do dia", font=("Arial", 12, "bold"), fg="blue", bg="light blue", bd=2, relief="solid" )
label_relacao_paginas.grid(row=7, column=4, columnspan=1, padx=8, pady=5)

#Label para a calculadora rapida
label_calculadora = tk.Label(window, text="calculadora rápida", font=("arial", 12, "bold"), fg="white", bg="blue", bd=2, relief="solid")
label_calculadora.grid(row=0, column=4, columnspan=1, padx=0, pady=0)

label_calculadora_c = tk.Label(window, text="Cópias:", font=("arial", 10, "bold"), fg="black")
label_calculadora_c.place(x=1000, y=90, width=50, height=30)
calculadora_c = tk.Entry(window, font=font_padrao, bg="white")
calculadora_c.place(x=1090, y=90, width=50, height=20)

label_calculadora_imp = tk.Label(window, text="Impressão:", font=("arial", 10, "bold"), fg="black")
label_calculadora_imp.place(x=990, y=128)
calculadora_imp = tk.Entry(window, font=font_padrao, bg="white")
calculadora_imp.place(x=1090, y=128, width=50, height=20)

label_calculadora_digit = tk.Label(window, text="Digitalização:", font=("arial", 10, "bold"), fg="black")
label_calculadora_digit.place(x=980, y=160)
calculadora_digit = tk.Entry(window, font=font_padrao, bg="white")
calculadora_digit.place(x=1090, y=160, width=50, height=20)

label_resultado_calc= tk.Label(window, font=("arial", 12, "bold"), fg="white", bg="blue")
label_resultado_calc.place(x=970, y=190, width=200, height=30)

# Botão para calcular e gerar o relatório final
btn_calcular = tk.Button(window, text="Calcular e Gerar Relatório", command=calcular_renda, bg="lightgreen", font=("Arial", 12, "bold"), relief="raised")
btn_calcular.grid(row=8, column=1, columnspan=2, pady=1)

# Botão para definir novos valores
btn_definir_novos_valores = tk.Button(window, text="Definir Novos Valores iniciais", command=janela_definir_novos_valores, bg="lightcoral", font=("Arial", 12, "bold"))
btn_definir_novos_valores.grid(row=9, column=1, columnspan=2, pady=3)

#botão para saber sobre o programa
btn_sobre = tk.Button(window, text="Sobre o programa", command=sobre, bg="yellow", font=("arial", 12, "bold"))
btn_sobre.grid(row=9, column=3, columnspan=2, pady=3 )

# Inicia o processo de atualização em tempo real
atualizar_resultado()

atualizar_valores_iniciais()

atualizar_relacao_paginas()

calculadora_rapida()

window.mainloop()

