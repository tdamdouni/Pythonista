#!/usr/bin/env python
# Written by: DGC

# python imports
import unittest

# local imports
import MVC

#==============================================================================
class utest_MVC(unittest.TestCase):
    
    def test_model(self):
        model = MVC.Model()
        question, possible_answers = model.question_and_answers()

        # can't test what they are because they're random
        self.assertTrue(
            isinstance(question, str),
            "Question should be a string"
            )
        self.assertTrue(
            isinstance(possible_answers, list),
            "Answers should be a list"
            )

        for item in possible_answers:
            self.assertTrue(
                isinstance(item[0], str),
                "Elements of possible answer list should be strings"
                )

    def test_controller(self):
        model = ModelMock()
        view = ViewMock()
        controller = MVC.Controller(model, view)
        controller.new_question()
        self.assertEqual(
            view.question,
            "Question", 
            "Controller should pass the question to the view."
            )
        controller.answer("Question", "correct")
        self.assertEqual(
            controller.view.mock_feedback,
            "That is correct.", 
            "The feedback for a correct answer is wrong."
            )
        controller.answer("Question", "incorrect")
        self.assertEqual(
            controller.view.mock_feedback,
            "Sorry that's wrong.", 
            "The feedback for an incorrect answer is wrong."
            )
        
    def test_view(self):
        view = MVC.View()
        controller = ControllerMock(view)
        view.register(controller)

        self.assertIs(
            view.answer_button, 
            None,
            "The answer button should not be set."
            )
        self.assertIs(
            view.continue_button,
            None,
            "The continue button should not be set."
            )
        view.new_question("Test", ["correct", "incorrect"])
        
        self.assertIsNot(
            view.answer_button, 
            None,
            "The answer button should be set."
            )
        self.assertIs(
            view.continue_button,
            None,
            "The continue button should not be set."
            )
        # simulate a button press
        view.answer_button.invoke()
        self.assertIs(
            view.answer_button, 
            None,
            "The answer button should not be set."
            )
        self.assertIsNot(
            view.continue_button,
            None,
            "The continue button should be set."
            )

        self.assertEqual(
            controller.question,
            "Test",
            "The question asked should be \"Test\"."
            )
        self.assertEqual(
            controller.answer,
            "correct",
            "The answer given should be \"correct\"."
            )
        
        # continue
        view.continue_button.invoke()
        self.assertIsNot(
            view.answer_button, 
            None,
            "The answer button should be set."
            )
        self.assertIs(
            view.continue_button,
            None,
            "The continue button should not be set."
            )

#==============================================================================
class ViewMock(object):
    
    def new_question(self, question, answers):
        self.question = question
        self.answers = answers

    def register(self, controller):
        pass

    def feedback(self, feedback):
        self.mock_feedback = feedback

#==============================================================================
class ModelMock(object):
    
    def question_and_answers(self):
        return ("Question", ["correct", "incorrect"])

    def is_correct(self, question, answer):
        correct = False
        if (answer == "correct"):
            correct = True
        return correct

#==============================================================================
class ControllerMock(object):
    
    def __init__(self, view):
        self.view = view

    def answer(self, question, answer):
        self.question = question
        self.answer = answer
        self.view.feedback("test")

    def next_question(self):
        self.view.new_question("Test", ["correct", "incorrect"])
    

#==============================================================================
if (__name__ == "__main__"):
    unittest.main(verbosity=2)
