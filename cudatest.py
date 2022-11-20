import torch


print(torch.__file__, torch.__path__, torch.__version__)
print(torch.cuda.is_available() )
other_played_cards_real = "DX"
if other_played_cards_real != "DX" or len(other_played_cards_real) == 4 and len(set(other_played_cards_real)) == 1:
    print("if is OK")
print(other_played_cards_real != "DX")
print(len(other_played_cards_real) == 4)
print(len(set(other_played_cards_real)) == 1)
print(other_played_cards_real != "DX" or len(other_played_cards_real) == 4 and len(set(other_played_cards_real)) == 1)
# not > and >or

for i in range(28):
    print("start " + "\"模拟器-" + str(i) + "\" cmd /k python portal.py ", i)

