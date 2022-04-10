class SkillShareIterator:
  def __iter__(self, base_url="https://www.skillshare.com/search?query=", count=2):
    self.base_url = base_url
    self.word = count*'a'

    return self

  def __next__(self):
    copy = self.word

    for i in reversed(range(0, len(self.word))):
      if self.word[i] >= 'z':
        self.word[i] = 'a'
      else:
        self.word[i] = chr(ord(self.word[i])+1)
        break

      print(i)

    return copy