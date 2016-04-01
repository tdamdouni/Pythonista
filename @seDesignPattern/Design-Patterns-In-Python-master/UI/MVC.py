#!/usr/bin/env python
# Written by: DGC

from Tkinter import *
import random

#==============================================================================
class Model(object):
    
    def __init__(self):
        # q_and_a is a dictionary where the key is a question and the entry is
        # a list of pairs, these pairs are an answer and whether it is correct
        self.q_and_a = {
            "How many wives did Henry VIII have?": [
                ("Five", False),
                ("Six", True),
                ("Seven", False),
                ("Eight", False)
                ],
            "In which Italian city is Romeo and Juliet primarily set?": [
                ("Verona", True),
                ("Naples", False),
                ("Milano", False),
                ("Pisa", False)
                ],
            "A light year is a measure of what?": [
                ("Energy", False),
                ("Speed", False),
                ("Distance", True),
                ("Intensity", False)
                ]
            }

    def question_and_answers(self):
        """ 
        Returns a randomly chosen question (string) and answers (list of 
        strings)  as a pair.
        """
        key = random.choice(self.q_and_a.keys())
        return (key, [x[0] for x in self.q_and_a[key]])

    def is_correct(self, question, answer):
        answers = self.q_and_a[question]
        for ans in answers:
            if (ans[0] == answer):
                return ans[1]
        assert False, "Could not find answer."

#==============================================================================
class View(object):

    def __init__(self):
        self.parent = Tk()
        self.parent.title("Trivia")

        self.initialise_ui()

        self.controller = None

    def clear_screen(self):
        """ Clears the screen deleting all widgets. """
        self.frame.destroy()
        self.initialise_ui()
        
    def initialise_ui(self):
        self.answer_button = None
        self.continue_button = None

        self.frame = Frame(self.parent)
        self.frame.pack()

    def new_question(self, question, answers):
        """ 
        question is a string, answers is a list of strings
        e.g
        view.new_question(
          "Is the earth a sphere?", 
          ["Yes", "No"]
        )
        """
        self.clear_screen()
        # put the question on as a label
        question_label = Label(self.frame, text=question)
        question_label.pack()

        # put the answers on as a radio buttons
        selected_answer = StringVar()
        selected_answer.set(answers[0])

        for answer in answers:
            option = Radiobutton(
                self.frame,
                text=answer,
                variable=selected_answer,
                value=answer,
                )
            option.pack()

        # button to confirm
        answer_function = lambda : self.controller.answer(
            question,
            selected_answer.get()
            )
        self.answer_button = Button(
            self.frame,
            text="Answer",
            command=answer_function
            )
        self.answer_button.pack()
        
    def main_loop(self):
        mainloop()

    def register(self, controller):
        """ Register a controller to give callbacks to. """
        self.controller = controller

    def feedback(self, feedback):
        self.clear_screen()
        label = Label(self.frame, text=feedback)
        label.pack()
        
        self.continue_button = Button(
            self.frame,
            text="Continue",
            command=self.controller.next_question
            )
        self.continue_button.pack()

#==============================================================================
class Controller(object):

    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.register(self)
        self.new_question()

    def new_question(self):
        q_and_a = self.model.question_and_answers()
        self.view.new_question(q_and_a[0], q_and_a[1])
        
    def next_question(self):
        self.new_question()
        
    def answer(self, question, answer):
        correct = self.model.is_correct(question, answer)
        feedback = ""
        if (correct):
            feedback = "That is correct."
        else:     
            feedback = "Sorry that's wrong."

        self.view.feedback(feedback)

#==============================================================================
if (__name__ == "__main__"):
    # Note: The view should not send to the model but it is often useful
    # for the view to receive update event information from the model. 
    # However you should not update the model from the view.

    view = View()
    model = Model()
    controller = Controller(model, view)

    view.main_loop()
    
