from konlpy.tag import Okt

okt = Okt()
text = okt.pos('부모가 과학자… 초등생이 과연 이 유전자 논문을 썼을까?')

print(text)



# arr = []

# arr.append({'key' : 'a', 'val' : 100 })
# arr.append({'key' : 'b', 'val' : 200 })
# arr.append({'key' : 'c', 'val' : 300 })
# arr.append({'key' : 'd', 'val' : 400 })

# search = list(filter(lambda x: x['key'] == 'c', arr))
# search[0]['val'] = 700

# print(arr)