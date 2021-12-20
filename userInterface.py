import tkinter as tk

black = "#121212"
white = "#FFFFFF"
lightBlue = "#BCCCDC"

font = ("MS Reference Sans Serif", 12)
fontBold = ("MS Reference Sans Serif", 11, "bold")


class userInterface:
    def __init__(self):
        self.window = tk.Tk()
        self.windowSetup()
        self.textSetup()
        self.sendButtonSetup()
        self.convoBoxSetup()


    def windowSetup(self):
        self.window.resizable(height=False, width=False)
        self.window.configure(height=400, width=600, bg=black)
        self.window.title("MyChatbotChum")

    def textSetup(self):
        self.text_box = tk.Entry(bg=black, font=font, fg=white, justify=tk.LEFT, insertbackground=black)
        self.text_box.place(relheight=0.1, relwidth=0.8, relx=0.01, rely=0.88)
        self.text_box.focus()
        self.text_box.bind('<Return>', self.onEnter)

    def sendButtonSetup(self):
        self.window.sendButton = tk.Button(bg=white, highlightthickness=0, font=fontBold, text="Enter",
                                    activebackground=lightBlue, command=self.onEnterButton)
        self.window.sendButton.place(relheight=0.1, relwidth=0.17, relx=0.82, rely=0.88)

    def convoBoxSetup(self):
        self.convoBox = tk.Text(bg=black, font=font, fg=white, cursor="arrow", state=tk.DISABLED, wrap=tk.WORD)
        self.convoBox.place(relheight=0.8, relwidth=0.95, relx=0.02, rely=0.05)
        scrollbar = tk.Scrollbar(self.convoBox, command=self.convoBox.yview())
        scrollbar.place(relheight=1, relx=0.97)

    def onEnter(self, event):
        text = event.widget.get()
        if not text:
            return
        userInterface.displayMessage(self, text, "You")

    def onEnterButton(self):
        text = self.text_box.get()
        if not text:
            return
        userInterface.displayMessage(self, text, "You")


    def displayMessage(self, text, sentFrom):
        self.text_box.delete(0, tk.END)
        message = str(sentFrom) + ": " + str(text) + "\n"
        self.convoBox.configure(state=tk.NORMAL)
        self.convoBox.insert(tk.END, message)
        self.convoBox.configure(state=tk.DISABLED)




        #delete and replace with AI reply
        #reply = str(sentFrom) + ": " + str(get_response(message)) + "\n"
        reply = str("Assistant: Fuck off Connor Stockbridge. He was done for noncing. He's a paedophile. Paedophile.\n")
        self.convoBox.configure(state=tk.NORMAL)
        self.convoBox.insert(tk.END, reply)
        self.convoBox.configure(state=tk.DISABLED)

    def runProgram(self):
        self.window.mainloop()




if __name__ == "__main__":
    chatbotInstance = userInterface()
    chatbotInstance.runProgram()



#text to speech for reply?
#different colours for human/bot