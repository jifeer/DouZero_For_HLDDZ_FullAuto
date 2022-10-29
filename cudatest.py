import torch
import pynvml

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

pynvml.nvmlInit()
# 这里的1是GPU id
handle = pynvml.nvmlDeviceGetHandleByIndex(1)
meminfo = pynvml.nvmlDeviceGetMemoryInfo(handle)
print(meminfo.total) #第二块显卡总的显存大小
print(meminfo.used)#这里是字节bytes，所以要想得到以兆M为单位就需要除以1024**2
print(meminfo.free) #第二块显卡剩余显存大小