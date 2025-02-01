local Workspace = game:GetService("Workspace")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local StarterGui = game:GetService("StarterGui")

local Player = Players.LocalPlayer
local Event = ReplicatedStorage:WaitForChild("event")
local Trainer = require(ReplicatedStorage:WaitForChild("trainer"))
local Events = require(Player:WaitForChild("PlayerGui"):WaitForChild("framework"):WaitForChild("events"))

local Beys = Workspace:WaitForChild("beyblades")
local Battles = Workspace:WaitForChild("battles")
local Specials = Workspace:WaitForChild("specials")

local LoopEnabled = true -- Começa ativo por padrão

function GetBey()
    local Bey = Beys:FindFirstChild(Player.Name)
    if Bey and Bey.PrimaryPart then
        return Bey
    end
    return nil
end

-- Evento para detectar quando uma batalha termina
Battles.ChildRemoved:Connect(function(A_1)
    if A_1 and A_1.Name == Player.Name .. "_Target" then
        task.wait(1) -- Espera 1 segundo antes de iniciar uma nova batalha
        if LoopEnabled then
            Event:FireServer("BattleTower")
        end
    end
end)

-- Dispara o evento do servidor para começar a batalha (se estiver ativado)
if LoopEnabled then
    Event:FireServer("BattleTower")
end

-- Evento para fechar o Trainer após o resultado da batalha
Events.TrainerBattleResult = function()
    task.wait()
    if Trainer and type(Trainer.close) == "function" then
        Trainer.close()
    end
end

-- Loop otimizado para atacar o inimigo automaticamente
RunService.Heartbeat:Connect(function()
    if LoopEnabled then
        local Bey = GetBey()
        if Bey then
            local Enemy = Beys:FindFirstChild(Player.Name .. "_Target")
            if Enemy then
                local Humanoid = Enemy:FindFirstChildOfClass("Humanoid")
                if Humanoid then
                    Humanoid.Health = 0
                end
            end
        end
    end
end)

-- Criando a interface gráfica
local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Parent = Player:WaitForChild("PlayerGui")

-- Botão para iniciar/parar o loop
local LoopButton = Instance.new("TextButton")
LoopButton.Parent = ScreenGui
LoopButton.Size = UDim2.new(0, 120, 0, 50)
LoopButton.Position = UDim2.new(0.85, 0, 0.1, 0) -- Canto superior direito
LoopButton.BackgroundColor3 = Color3.fromRGB(50, 50, 50)
LoopButton.TextColor3 = Color3.fromRGB(255, 255, 255)
LoopButton.Text = "Parar Loop"

-- Alternar loop ao clicar no botão
LoopButton.MouseButton1Click:Connect(function()
    LoopEnabled = not LoopEnabled
    LoopButton.Text = LoopEnabled and "Parar Loop" or "Iniciar Loop"
end)

-- Criando o botão móvel que mostra o andar mais alto alcançado
local HighestFloorButton = Instance.new("TextButton")
HighestFloorButton.Parent = ScreenGui
HighestFloorButton.Size = UDim2.new(0, 200, 0, 50)
HighestFloorButton.Position = UDim2.new(0.7, 0, 0.2, 0) -- Posição inicial
HighestFloorButton.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
HighestFloorButton.TextColor3 = Color3.fromRGB(255, 255, 255)
HighestFloorButton.TextScaled = true
HighestFloorButton.Text = "Andar mais alto: 0"
HighestFloorButton.Draggable = true -- Torna o botão móvel

-- Função para atualizar o botão com o andar mais alto
local function UpdateHighestFloor()
    while task.wait(1) do -- Atualiza a cada 1 segundo
        local Stats = Player:FindFirstChild("stats")
        if Stats then
            local TowerStats = Stats:FindFirstChild("tower")
            if TowerStats then
                local HighestFloor = TowerStats:FindFirstChild("highest")
                if HighestFloor then
                    HighestFloorButton.Text = "Andar mais alto: " .. HighestFloor.Value
                end
            end
        end
    end
end

-- Inicia a atualização do botão em uma nova thread
task.spawn(UpdateHighestFloor)

-- Script Anti-AFK
local AntiAFKGui = Instance.new("ScreenGui")
local AntiAFKLabel = Instance.new("TextLabel")
local AntiAFKStatus = Instance.new("TextLabel")

AntiAFKGui.Parent = game.CoreGui
AntiAFKGui.ZIndexBehavior = Enum.ZIndexBehavior.Sibling

AntiAFKLabel.Parent = AntiAFKGui
AntiAFKLabel.Active = true
AntiAFKLabel.BackgroundColor3 = Color3.new(0.176, 0.176, 0.176)
AntiAFKLabel.Draggable = true -- Permite mover
AntiAFKLabel.Position = UDim2.new(0.7, 0, 0.1, 0)
AntiAFKLabel.Size = UDim2.new(0, 370, 0, 52)
AntiAFKLabel.Font = Enum.Font.SourceSansSemibold
AntiAFKLabel.Text = "Anti AFK"
AntiAFKLabel.TextColor3 = Color3.new(0, 1, 1)
AntiAFKLabel.TextSize = 22

AntiAFKStatus.Parent = AntiAFKLabel
AntiAFKStatus.BackgroundColor3 = Color3.new(0.176, 0.176, 0.176)
AntiAFKStatus.Position = UDim2.new(0, 0, 1, 0)
AntiAFKStatus.Size = UDim2.new(0, 370, 0, 44)
AntiAFKStatus.Font = Enum.Font.ArialBold
AntiAFKStatus.Text = "Status: Active"
AntiAFKStatus.TextColor3 = Color3.new(0, 1, 1)
AntiAFKStatus.TextSize = 20

local VirtualUser = game:GetService("VirtualUser")
game:GetService("Players").LocalPlayer.Idled:Connect(function()
    VirtualUser:CaptureController()
    VirtualUser:ClickButton2(Vector2.new())
    AntiAFKStatus.Text = "Roblox tentou te expulsar, mas EU BOTEI ELE PRA MAMAR"
    wait(4)
    AntiAFKStatus.Text = "Status: ATIVO"
end)
