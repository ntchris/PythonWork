
import string
import unittest

# now can use bool startswith()  and bool endswith()
def isStringEndingWith(str, substr):
    print(str + "  " + substr)
    foundIndex = str.rfind(substr)
    if(foundIndex < 0):
        return False
    
    size = len(str)
    subsize = len(substr)
    expectedSubStrIndex = size - subsize    
    return foundIndex == expectedSubStrIndex 


def isStringStartsgWith(str, substr):
    print(str + "  " + substr)
    foundIndex = str.find(substr)

    return foundIndex == 0


class TestStringMethods(unittest.TestCase):

  def test_str_start_abc_a(self):
        self.assertEqual(isStringStartsgWith("abc", "a"), True)
        
  def test_str_start_abcd_abc(self):
       self.assertEqual(isStringStartsgWith("abcd", "abc"), True)

  def test_str_start_abcd_abcd(self):
       self.assertEqual(isStringStartsgWith("abcd", "abcd"), True)
         
  def test_str_start_abcd_b(self):
       self.assertEqual(isStringStartsgWith("abcd", "b"), False)
       
  def test_str_start_abc_d(self):
       self.assertEqual(isStringStartsgWith("abc", "d"), False)
  
  def test_str_start_abcd_bcd(self):
       self.assertEqual(isStringStartsgWith("abcd", "bcd"), False)
               
  ## *************************************************               
        
  def test_str_ending_abc_c(self):
        self.assertEqual(isStringEndingWith("abc", "c"), True)
  
  def test_str_ending_abcd_bcd(self):
        self.assertEqual(isStringEndingWith("abcd", "bcd"), True)
        
  def test_str_ending_abc_a(self):
        self.assertEqual(isStringEndingWith("abc", "a"), False)
        
  def test_str_ending_abc_d(self):      
        self.assertEqual(isStringEndingWith("abc", "d"), False)
          
  def test_str_ending_abc_b(self):
        self.assertEqual(isStringEndingWith("abc", "b"), False)
  
  def test_str_ending_abc_ab(self):
        self.assertEqual(isStringEndingWith("abc", "ab"), False)        
        
  def test_str_ending_abc_abc(self):
        self.assertEqual(isStringEndingWith("abc", "abc"), True)

  def test_str_ending_abc_abcd(self):
        self.assertEqual(isStringEndingWith("abc", "abcd"), False)


def main():
   return

  
main()
