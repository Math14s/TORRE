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

-- Criando o botão flutuante
local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Parent = Player:WaitForChild("PlayerGui")

local Button = Instance.new("TextButton")
Button.Parent = ScreenGui
Button.Size = UDim2.new(0, 120, 0, 50)
Button.Position = UDim2.new(0.85, 0, 0.1, 0) -- Canto superior direito
Button.BackgroundColor3 = Color3.fromRGB(50, 50, 50)
Button.TextColor3 = Color3.fromRGB(255, 255, 255)
Button.Text = "Parar Loop"

-- Alternar loop ao clicar no botão
Button.MouseButton1Click:Connect(function()
    LoopEnabled = not LoopEnabled
    Button.Text = LoopEnabled and "Parar Loop" or "Iniciar Loop"
end)
