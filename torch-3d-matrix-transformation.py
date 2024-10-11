import torch
import time

# Example world coordinates (3xN)
torch.cuda.synchronize()  # Ensure all prior GPU work is done
t0 = time.time()
world_coords = torch.rand(3, int(3e8), device='cuda')
ones = torch.ones(1, world_coords.shape[1], device='cuda')
homogeneous_coords = torch.vstack((world_coords, ones))
torch.cuda.synchronize()  # Ensure all prior GPU work is done
t1 = time.time()
print(f'Completed random assignment in {(t1-t0):.3f}s.')

# Your homogeneous transformation matrix (4x4)
transform = torch.rand(4, 4, device='cuda')
transform[3] = torch.tensor([0, 0, 0, 1], device='cuda')
inverse_transform = torch.linalg.inv(transform)
torch.cuda.synchronize()  # Ensure all prior GPU work is done
t2 = time.time()
print(f'Completed transformation matrix in {(t2-t1):.3f}s.')

# Apply the transformation
camera_coords = inverse_transform @ homogeneous_coords
camera_coords = camera_coords[:3] / camera_coords[3]
torch.cuda.synchronize()  # Ensure all prior GPU work is done
t3 = time.time()
print(f'Completed matrix multiplications in {(t3-t2):.3f}s.')

# Move results to CPU if needed
camera_coords = camera_coords.cpu()
