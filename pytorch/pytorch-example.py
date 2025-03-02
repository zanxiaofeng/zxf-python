import torch
torch.cuda.is_available()

tr1 = torch.rand(5, 3)

tr1.size()
tr1.type()

tr1.max()
torch.max(tr1)
tr1.min()
torch.min(tr1)
tr1.sin()
torch.sin(tr1)
tr1.cos()
torch.cos(tr1)
tr1.tan()
torch.tan(tr1)
tr1.sum()
torch.sum(tr1)
tr1.sqrt()
torch.sqrt(tr1)
tr1.pow(3)
torch.pow(tr1, 3)
tr1.log()
torch.log(tr1)

tr2 = torch.rand(5, 3)
tr1 + tr2
tr1 - tr2
tr1 * tr2
tr1 / tr2
tr1 % tr2

