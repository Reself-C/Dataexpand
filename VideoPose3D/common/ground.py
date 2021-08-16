import torch

def ground_computer(foot):
    return torch.stack([single_ground_computer(foot[i]) for i in range(foot.shape[0])])

def single_ground_computer(single_foot):
    b = torch.ones((single_foot.shape[0],1),device='cuda:0' if torch.cuda.is_available else 'cpu')
    A = single_foot
    A_T = A.T
    A_2 = torch.linalg.inv(torch.matmul(A_T,A))
    ground = torch.matmul(torch.matmul(A_2, A_T),b)
    # ax + by + cz = 1
    # ground [a, b, c]
    return ground
