dir(document) 
div = document.CreateElement("div")
div.innerHTML = "Hello from Python!"
document.Body.AppendChild(div)
div.id = "message"
div.SetStyleAttribute("font-size", "24px")
def say_ouch(o, e):
    o.innerHTML = "Ouch!"

document.message.events.onclick += say_ouch