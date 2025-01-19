import sys
import time
import random
import os
import json  # Para manipulação de arquivos JSON
import threading
import requests
import subprocess
import platform

ARQUIVO_JSON = "progresso_jogo.json"

# URL do leaderboard
url_leaderboard = "http://rankandar.ddns.net:5000/"

# URL do endpoint do site da leaderboard
URL_LEADERBOARD = "http://rankandar.ddns.net:5000/atualizar"

class JogoIncremental:
    def __init__(self):
        # Verifica se existe um arquivo de progresso salvo
        self.nick = ""
        self.carregar_progresso()
        if not self.nick:
           self.limpar_tela()
           self.nick = input("Digite o nome do seu personagem: ").strip()
           self.limpar_tela()

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela no Termux e Windows

    def abrir(self):
        try:
            url = "http://170.83.227.128:5000/"
            subprocess.run(["termux-open", url])
            print("Abrindo o leaderboard no navegador...")
            time.sleep(2)
        except Exception as e:
            print(f"Erro ao abrir o leaderboard: {e}")
            time.sleep(2)

    def atualizar_leaderboard(self):
         try:
        # Lendo o arquivo JSON
            with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
                progresso = json.load(f)

        # Extraindo as informações necessárias
            nick = progresso.get("nick")
            maior_andar = progresso.get("maior_andar", 0)

            if not nick or maior_andar <= 0:
                print("Dados inválidos no arquivo JSON.")
                return

        # Enviando os dados para o site
            payload = {"nick": nick, "maior_andar": maior_andar}
            response = requests.post(URL_LEADERBOARD, json=payload)

            if response.status_code == 200:
                print("Leaderboard atualizada com sucesso!")
            else:
                print(f"Falha ao atualizar leaderboard: {response.text}")
         except Exception as e:
            print(f"Erro ao processar o arquivo JSON: {e}")

    def spin(self):
        spinner = ['|', '/', '-', '\\']  # Caracteres para criar o efeito de rotação
        try:
          for _ in range(5):  # Número de iterações
            for char in spinner:
                sys.stdout.write(f'\r {char}')  # Atualiza a animação
                sys.stdout.flush()  # Garante atualização instantânea no terminal
                time.sleep(0.1)
        finally:
          sys.stdout.write('\r' + ' ' * 20 + '\r')  # Limpa a linha ao final

    def salvar_progresso(self):
        # Cria um dicionário com o status atual do jogador
        progresso = {
            'nick': self.nick,
            'vida': self.vida,
            'forca': self.forca,
            'agilidade': self.agilidade,
            'ouro': self.ouro,
            'pontos_disponiveis': self.pontos_disponiveis,
            'arma_equipada': self.arma_equipada,
            'bota_equipada': self.bota_equipada,
            'colete_equipado': self.colete_equipado,
            'maior_andar': self.maior_andar,
            'vitorias': self.vitorias,
            'derrotas': self.derrotas,
            'recordes_ouro': self.recordes_ouro,
            'andar_atual': self.andar_atual
        }
        # Salva o progresso em um arquivo JSON
        with open("progresso_jogo.json", "w") as arquivo:
            json.dump(progresso, arquivo)
        time.sleep(1)
        print("Progresso salvo com sucesso!")

    def carregar_progresso(self):
        # Tenta carregar o progresso salvo, se existir
        if os.path.exists("progresso_jogo.json"):
            with open("progresso_jogo.json", "r") as arquivo:
                progresso = json.load(arquivo)
                # Restaura o status do jogador a partir do arquivo
                self.nick = progresso.get('nick', "")
                self.vida = progresso['vida']
                self.forca = progresso['forca']
                self.agilidade = progresso['agilidade']
                self.ouro = progresso['ouro']
                self.pontos_disponiveis = progresso['pontos_disponiveis']
                self.arma_equipada = progresso['arma_equipada']
                self.bota_equipada = progresso['bota_equipada']
                self.colete_equipado = progresso['colete_equipado']
                self.maior_andar = progresso['maior_andar']
                self.vitorias = progresso['vitorias']
                self.derrotas = progresso['derrotas']
                self.recordes_ouro = progresso['recordes_ouro']
                self.andar_atual = progresso['andar_atual']
            self.limpar_tela()
            print(f"    CARREGANDO PROGRESSO SALVO ")
            self.spin()
            time.sleep(2)
            self.limpar_tela()
            print(f"SEJA BEM-VINDO(a) á TORRE! {self.nick.upper()}")
            time.sleep(3)
        else:
            # Se não existir um progresso salvo, inicializa com valores padrões
            self.nick = ""
            self.vida = 500
            self.forca = 100
            self.agilidade = 25
            self.ouro = 5
            self.pontos_disponiveis = 10
            self.arma_equipada = None
            self.bota_equipada = None
            self.colete_equipado = None
            self.maior_andar = 0
            self.vitorias = 0
            self.derrotas = 0
            self.recordes_ouro = 0
            self.andar_atual = 1

    def menu(self):
        while True:
            self.limpar_tela()
            print(f"==== INICIO ====")
            # Exibe a vida com o multiplicador do colete equipado, se houver
            if self.colete_equipado:
                vida_com_buff = self.vida * self.colete_equipado[1]
                print(f"Vida: {vida_com_buff} (buff do colete: {self.colete_equipado[1]}x)")
            else:
                print(f"Vida: {self.vida}")

            # Exibe a força com o multiplicador da arma equipada, se houver
            if self.arma_equipada:
                forca_com_buff = self.forca * self.arma_equipada[1]
                print(f"Força: {forca_com_buff} (buff da arma: {self.arma_equipada[1]}x)")
            else:
                print(f"Força: {self.forca}")

            # Exibe a agilidade com o multiplicador da bota equipada, se houver
            if self.bota_equipada:
                agilidade_com_buff = self.agilidade * self.bota_equipada[1]
                print(f"Agilidade: {agilidade_com_buff} (buff da bota: {self.bota_equipada[1]}x)")
            else:
                print(f"Agilidade: {self.agilidade}")

            print(f"Ouro: {self.ouro}")
            print(f"Pontos Disponíveis: {self.pontos_disponiveis}")
            print("-----Menu-----")
            print("1. Loja")
            print("2. Inventário")
            print("3. Distribuir status")
            print("4. Torre")
            print("5. Seus Recordes")
            print("6. Ver Rank Global")
            print("7. Sair")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.loja()
            elif opcao == "2":
                self.inventario()
            elif opcao == "3":
                self.distribuir_status()
            elif opcao == "4":
                self.torre()
            elif opcao == "5":
                self.mostrar_recordes()
            elif opcao == "6":
            	self.atualizar_leaderboard()
            	self.abrir()
            elif opcao == "0":
                self.salvar_progresso()
                self.atualizar_leaderboard()
            elif opcao == "7":
                self.limpar_tela()
                print(f"Salvando progresso... ")
                self.spin()
                self.salvar_progresso()
                self.atualizar_leaderboard()
                print(f"\nSaindo do jogo... ")
                time.sleep(2)
                break
            else:
                print("Opção inválida.")
                time.sleep(1)

    def minigame_pedra_papel_tesoura(self):
        opcoes = ["pedra", "papel", "tesoura"]
        vitorias_jogador = 0
        vitorias_boss = 0
        rodadas = 5

        for rodada in range(rodadas):
            print(f"\nRodada {rodada + 1} de {rodadas}")
            escolha_boss = random.choice(opcoes)
            escolha_jogador = input("Escolha pedra, papel ou tesoura: ").lower()

            if escolha_jogador not in opcoes:
                print("Escolha inválida! O boss ganhou esta rodada.")
                vitorias_boss += 1
                continue

            print(f"Você escolheu {escolha_jogador}, o boss escolheu {escolha_boss}.")

            if escolha_jogador == escolha_boss:
                print("Empate!")
            elif (
                (escolha_jogador == "pedra" and escolha_boss == "tesoura") or
                (escolha_jogador == "tesoura" and escolha_boss == "papel") or
                (escolha_jogador == "papel" and escolha_boss == "pedra")
            ):
                print("Você ganhou esta rodada!")
                vitorias_jogador += 1
            else:
                print("O boss ganhou esta rodada!")
                vitorias_boss += 1

            time.sleep(1)

        print("\nResultado Final:")
        print(f"Você: {vitorias_jogador} | Boss: {vitorias_boss}")
        if vitorias_jogador > vitorias_boss:
            print("Você venceu o RAID BOSS!")
            return True
        else:
            print("Você perdeu para o RAID BOSS!")
            return False

    def inventario(self):
        self.limpar_tela()
        print("==== INVENTARIO ====")
        if self.arma_equipada:
            print(f"Arma: {self.arma_equipada[0]} (multiplicador {self.arma_equipada[1]}x)")
        if self.bota_equipada:
            print(f"Bota: {self.bota_equipada[0]} (multiplicador {self.bota_equipada[1]}x)")
        if self.colete_equipado:
            print(f"Colete: {self.colete_equipado[0]} (multiplicador {self.colete_equipado[1]}x)")

        input("...")

    def distribuir_status(self):
        while True:
            self.limpar_tela()
            print(f"==== DISTRIBUIR ====")
            print(f"PONTOS DISPONÍVEIS: {self.pontos_disponiveis}")
            print("1. Vida")
            print("2. Força")
            print("3. Agilidade")
            print("4. Voltar")

            # Verifica se ainda há pontos disponíveis
            if self.pontos_disponiveis == 0:
                print("Você não tem mais pontos para distribuir.")
                time.sleep(2)
                break

            escolha = input("Escolha um status para colocar pontos: ")
            if escolha == "4":
                break

            if escolha not in ["1", "2", "3"]:
                print("Opção inválida!")
                time.sleep(1)
                continue

            try:
                pontos = int(input("Quantos pontos? "))
                if pontos <= 0:
                    print("Você deve adicionar ao menos 1 ponto!")
                    time.sleep(1)
                    continue
            except ValueError:
                print("Entrada inválida! Digite um número inteiro.")
                time.sleep(1)
                continue

            if pontos > self.pontos_disponiveis:
                print("\nVocê não tem pontos suficientes!")
                time.sleep(2)
                continue

            # Atualiza os status de acordo com a escolha
            if escolha == "1":
                self.vida += pontos
            elif escolha == "2":
                self.forca += pontos
            elif escolha == "3":
                self.agilidade += pontos

            self.pontos_disponiveis -= pontos  # Reduz os pontos disponíveis
            print(f"Você adicionou {pontos} ponto(s)!")
            time.sleep(1)

        print("Distribuição de status concluída.")

    def loja(self):
        while True:
            self.limpar_tela()
            print("==== LOJA ====")
            print(f"Ouro: {self.ouro}")
            print("Escolha uma categoria:")
            print("1. Armas")
            print("2. Botas")
            print("3. Coletes")
            print("4. Voltar")

            opcao = input("Escolha uma opção: ")
            if opcao == "1":
                self.loja_armas()
            elif opcao == "2":
                self.loja_botas()
            elif opcao == "3":
                self.loja_coletes()
            elif opcao == "4":
                return
            else:
                print("Opção inválida!")
                time.sleep(1)

    def mostrar_recordes(self):
        self.limpar_tela()
        print("==== SEUS RECORDES ====")
        print(f"Maior Andar Alcançado: {self.maior_andar}")
        print(f"Vitórias: {self.vitorias}")
        print(f"Derrotas: {self.derrotas}")
        input("Pressione Enter para voltar ao menu.")

    def loja_armas(self):
        self.limpar_tela()
        print("==== LOJA DE ARMAS ====")
        print(f"Ouro: {self.ouro}")
        print("1. 10 Ouro - Espada de madeira (1.5x força)")
        print("2. 50 Ouro - Espada de pedra (3x força)")
        print("3. 200 Ouro - Espada de ferro (5x força)")
        print("4. 500 Ouro - Sabre Comum (10x força)")
        print("5. 800 Ouro - Sabre de Aço (20x força)")
        print("6. 1200 Ouro - Sabre de Luz (50x força)")
        print("7. 2000 Ouro - Excalibur (100x força)")
        print("8. Voltar")

        escolha = input("Escolha uma opção: ")

        if escolha == "8":
            return

        if escolha == "1" and self.ouro >= 10:
            self.ouro -= 10
            self.arma_equipada = ("Espada de madeira", 1.5)
        elif escolha == "2" and self.ouro >= 50:
            self.ouro -= 50
            self.arma_equipada = ("Espada de pedra", 3)
        elif escolha == "3" and self.ouro >= 200:
            self.ouro -= 200
            self.arma_equipada = ("Espada de ferro", 5)
        elif escolha =="22042008" and self.ouro>= 0:
            self.arma_equipada = ("Dragon Slayer", 200)
        elif escolha == "4" and self.ouro >= 500:
            self.ouro -= 500
            self.arma_equipada = ("Sabre Comum", 10)
        elif escolha == "5" and self.ouro >= 500:
            self.ouro -= 500
            self.arma_equipada = ("Sabre De Aço", 20)
        elif escolha == "6" and self.ouro >= 800:
            self.ouro -= 800
            self.arma_equipada = ("Sabre de Luz", 50)
        elif escolha == "7" and self.ouro >= 2000:
            self.ouro -= 2000
            self.arma_equipada = ("Excalibur", 100)
        elif escolha == "desentupidor" and self.ouro >= 0:
            self.arma_equipada = ("🪠", 150)
        else:
            print("Ouro insuficiente ou opção inválida.")
            time.sleep(2)
            return

        print(f"Arma equipada: {self.arma_equipada[0]} com multiplicador {self.arma_equipada[1]}x de força.")
        time.sleep(1)

    def loja_botas(self):
        self.limpar_tela()
        print("==== LOJA DE BOTAS ====")
        print(f"Ouro: {self.ouro}")
        print("1. 70 Ouro - Bota Ágil (2x Agi)")
        print("2. 150 Ouro - Bota Booster (4x Agi)")
        print("3. 300 Ouro - Bota Sonica (10x Agi)")
        print("4. 500 Ouro - Bota de aquiles (25x Agi)")
        print("5. 777 Ouro - Bota Speed Light (60x Agi)")
        print("6. 1000 Ouro - Bota Teleport (100x Agi)")
        print("7. 4500 Ouro - Tênis da Nike (300x Agi)")
        print("8. Voltar")

        escolha = input("Escolha uma opção: ")

        if escolha == "8":
            return

        if escolha == "1" and self.ouro >= 70:
            self.ouro -= 70
            self.bota_equipada = ("Bota Ágil", 2)
        elif escolha == "2" and self.ouro >= 150:
            self.ouro -= 150
            self.bota_equipada = ("Bota Booster", 4)
        elif escolha == "3" and self.ouro >= 300:
            self.ouro -= 300
            self.bota_equipada = ("Bota Sonica", 10)
        elif escolha == "4" and self.ouro >= 500:
            self.ouro -= 500
            self.bota_equipada = ("Bota de Aquiles", 25)
        elif escolha == "5" and self.ouro >= 777:
            self.ouro -= 777
            self.bota_equipada = ("Bota Light Speed", 60)
        elif escolha == "6" and self.ouro >= 1000:
            self.ouro -= 1000
            self.bota_equipada = ("Bota teleport", 100)
        elif escolha == "7" and self.ouro >= 4500:
            self.ouro -= 4500
            self.bota_equipada = ("Tênis da Nike", 300)
        elif escolha == "22042008" and self.ouro >= 0:
             self.bota_equipada = ("Salto Alto Rosa", 777)
        else:
            print("Ouro insuficiente ou opção inválida.")
            time.sleep(2)
            return

        print(f"Bota equipada: {self.bota_equipada[0]} com multiplicador {self.bota_equipada[1]}x de agilidade.")
        time.sleep(1)

    def loja_coletes(self):
        self.limpar_tela()
        print("==== LOJA DE COLETES ====")
        print(f"Ouro: {self.ouro}")
        print("1. 100 Ouro - Colete Padrão (3x Vida)")
        print("2. 300 Ouro - Colete Kevlar (6x Vida)")
        print("3. 800 Ouro - Colete Anti-Tanque (20x Vida)")
        print("4. 1500 Ouro - Colete Adamantium (70x Vida)")
        print("5. 3000 Ouro - Colete Vibranium (150x vida)")
        print("6. 6666 Ouro - Colete Infernal (666x Vida)")
        print("7. 7777 Ouro - Colete Divino (1000x Vida)")
        print("8. Voltar")

        escolha = input("Escolha uma opção: ")

        if escolha == "8":
            return

        if escolha == "1" and self.ouro >= 100:
            self.ouro -= 100
            self.colete_equipado = ("Colete Padrão", 3)
        elif escolha == "2" and self.ouro >= 300:
            self.ouro -= 300
            self.colete_equipado = ("Colete Kevlar", 6)
        elif escolha == "3" and self.ouro >= 800:
            self.ouro -= 800
            self.colete_equipado = ("Colete de Anti-Tanque", 20)
        elif escolha == "4" and self.ouro >= 1500:
            self.ouro -= 1500
            self.colete_equipado = ("Colete Adamantium", 70)
        elif escolha == "5" and self.ouro >= 3000:
            self.ouro -= 3000
            self.colete_equipado = ("Colete Vibranium", 150)
        elif escolha == "6" and self.ouro >= 6666:
            self.ouro -= 6666
            self.colete_equipado = ("Colete Infernal", 666)
        elif escolha == "7" and self.ouro >= 7777:
            self.ouro -= 7777
            self.colete_equipado = ("Colete Divino", 777)
        elif escolha == "22042008" and self.ouro >= 0:
            self.colete_equipado = ("Colete Baleado da PM", 0.1)
        else:
            print("Ouro insuficiente ou opção inválida.")
            time.sleep(2)
            return

        print(f"Colete equipado: {self.colete_equipado[0]} com multiplicador {self.colete_equipado[1]}x de vida.")
        time.sleep(1)

    def mostrar_sequencia(self, sequencia):
        # Exibe a sequência por 3 segundos
        for letra in sequencia:
            print(letra, end=' ', flush=True)
            time.sleep(0.5)
        time.sleep(2)
        self.limpar_tela()  # Limpa a tela

    def minigame_memoria(self):
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        def temporizador(resposta_event):
            time.sleep(7)  # 5 segundos para responder
            if not resposta_event.is_set():  # Verifica se a resposta foi dada
                print("\nTempo esgotado! Você perdeu!")
                resposta_event.set()  # Marca como respondido para finalizar
                return False

        for fase in range(1, 4):  # Três fases
            # Gerar uma sequência diferente para cada fase
            tamanho_sequencia = 5 + fase  # Aumenta o tamanho a cada fase
            sequencia = random.choices(letras, k=tamanho_sequencia)
            time.sleep(2)
            self.limpar_tela()
            time.sleep(2)
            print("3")
            time.sleep(1)
            print("2")
            time.sleep(1)
            print("1")
            time.sleep(1)
            print("Começou!")
            time.sleep(1)
            self.limpar_tela()
            print(f"\nFase {fase}: Memorize a sequência!")
            self.mostrar_sequencia(sequencia)

            # Preparar o temporizador e capturar a resposta
            resposta_event = threading.Event()
            thread_tempo = threading.Thread(target=temporizador, args=(resposta_event,))
            thread_tempo.start()

            tentativa = input("Digite a sequência que você viu: ").upper()
            resposta_event.set()  # Indica que o jogador respondeu a tempo

            thread_tempo.join()  # Aguarda o fim do temporizador

            if tentativa != ''.join(sequencia):
                print("Você errou a sequência!")
                time.sleep(1)
                return False

            print(f"Fase {fase} completa! Prepare-se para a próxima fase." if fase < 3 else "Você venceu o boss!")
            time.sleep(1)

        return True  # Venceu todas as fases

    def torre(self):
        while True:
            self.limpar_tela()
            print(f"==== ANDAR {self.andar_atual} ====")
            print("Lutando...")
            time.sleep(1)

            if self.arma_equipada:
                dano = self.forca * self.arma_equipada[1]
            else:
                dano = self.forca
            if self.bota_equipada:
                agilidade = self.agilidade * self.bota_equipada[1]
            else:
                agilidade = self.agilidade

            if self.colete_equipado:
                vida = self.vida * self.colete_equipado[1]
            else:
                vida = self.vida

            chance_vitoria = random.random()
            dificuldade = 0.2 * self.andar_atual * 2
            chance_de_vencer = (vida / 200) + (agilidade / 100) + (dano / 100) - dificuldade

            if self.andar_atual % 100 == 0:  # RAID BOSS a cada 100 andares
                self.limpar_tela()
                print("             RAID BOSS ENCONTRADO!")
                print("Para derrotar o RAID BOSS você precisa ganhar do BOSS em 5 turnos de PEDRA PAPEL E TESOURA")
                input("\n\nPressione ENTER para iniciar o combate...")
                if not self.minigame_pedra_papel_tesoura():
                    print("Voltando para o primeiro andar.")
                    self.derrotas += 1
                    self.andar_atual = 1
                    time.sleep(3)
                    break
                else:
                    self.ouro += self.andar_atual * 1.5  # Grande recompensa por vencer o RAID BOSS
                    self.pontos_disponiveis += 10
                    self.andar_atual += 1
                    time.sleep(3)
                    continue

            if chance_vitoria < chance_de_vencer:
                print("VITÓRIA! SUBINDO UM ANDAR")
                self.ouro += self.andar_atual
                self.pontos_disponiveis += 3
                self.vitorias += 1
                self.maior_andar = max(self.maior_andar, self.andar_atual)
                self.andar_atual += 1

                if self.andar_atual % 10 == 0:
                    self.limpar_tela()
                    print("                 BOSS ENCONTRADO!")
                    input("\n Você vai jogar um jogo da memoria para vencer o boss \n\n Pressione Enter para enfrentar o BOSS...")
                    if not self.minigame_memoria():  # Se o minigame for perdido
                        print("Você perdeu o desafio e será derrotado!")
                        self.derrotas += 1
                        self.andar_atual = 1  # Reseta para o andar 1 após derrota no boss
                        time.sleep(2)
                        break
            else:
                print("DERROTA! Você perdeu e voltará para o primeiro andar.")
                self.derrotas += 1
                self.andar_atual = 1  # Resetando para o andar 1 após derrota
                time.sleep(3)
                break

            print(f"RECOMPENSAS: {self.ouro} OURO e 3 PONTOS")
            time.sleep(3)

def iniciar():
    jogo = JogoIncremental()
    jogo.menu()

if __name__ == "__main__":
   iniciar()


