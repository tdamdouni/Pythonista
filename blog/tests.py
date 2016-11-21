import os
from datetime import datetime
import unittest
from blok import get_post_dict, create_post

class test_post_creation(unittest.TestCase):
  
  def setUp(self):
    self.post = 'title: Test\ndate: 30/04/2015\nslug: test-post\n====\nThis is a test'
  
  def remove_test_post(self):
    try:
      os.remove('posts/30-04-2015-test-post.markdown')
    except OSError:
      print('Failed to remove test post')
      
  def does_file_exist(self, filename):
    try:
      with open(filename, 'r') as f:
        f.read()   
    except IOError:
      return False
      
    return True
    
  def test_get_dict_parses_post_correctly(self):
    self.assertEqual(get_post_dict(self.post),  {'date': '30/04/2015', 'post': 'This is a test', 'slug': 'test-post', 'title': 'Test'})
    
  
  def test_file_creation(self):
    self.assertTrue(create_post(self.post))
    self.assertTrue(self.does_file_exist('posts/30-04-2015-test-post.markdown'), True)
    self.remove_test_post()
    
  def test_invalid_post_with_no_title_returns_false(self):
    post = 'Test\ndate: 30/04/2015\nslug: test-post\n====\nThis is a test'
    self.assertFalse(create_post(post))
    
    
  def test_invalid_blank_post_returns_false(self):
    post = ''
    self.assertFalse(create_post(post))
    
class test_templater(unittest.TestCase):
  
    

#if __name__ == '__main__':
#  unittest.main()

suite = unittest.TestLoader().loadTestsFromTestCase(test_post_creation)
unittest.TextTestRunner(verbosity=2).run(suite)

suite2 = unittest.TestLoader().loadTestsFromTestCase(test_post_creation)

#def test_file_creation()
#  post = 'title: Test\ndate: 30/04/2015\nslug: test-post\n====\nThis is a test'
#  success = create_post(post)
#  print(success)
