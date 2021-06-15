import numpy as np
import torch

torch.set_default_tensor_type(torch.DoubleTensor)

class Camera:

    def __init__(self,frames) -> None:
        '''
        Constructing an object of Camera class, defining its frame number, default rigid-body motion parameters
        '''

        self.frame = frames;
        x_default = np.linspace(-200,200,frames,dtype = np.float16).reshape(frames,1);
        y_default = np.array([np.random.randint(200)]*frames,dtype = np.float16).reshape(frames,1);
        z_default = np.array([np.random.randint(200)]*frames,dtype = np.float16).reshape(frames,1);
        self.camera_pos = np.concatenate((np.concatenate((x_default,y_default),1),z_default),1);

        dir_x_default = np.array([2 * np.pi * np.random.random()]*frames,dtype = np.float16).reshape(frames,1);
        dir_y_default = np.array([2 * np.pi * np.random.random()]*frames,dtype = np.float16).reshape(frames,1);
        dir_z_default = np.array([2 * np.pi * np.random.random()]*frames,dtype = np.float16).reshape(frames,1);
        self.camera_arg = np.concatenate((np.concatenate((dir_x_default,dir_y_default),1),dir_z_default),1);

        
        '''
        Gernerate extrinsics and intrinsics camera matrix from its default parameter
        These matrix could be updated later
        '''
        Camera.exmat_generator(self);
        Camera.inmat_generator(self);
        print("Camera initiallized!");
        

        pass
    
    def exmat_generator(self):
        '''
        Generate extrinsics matrix, used for transform the object in homogeneous world coordinate into homogeneous camera coordinate
        
        H_o2k = [ R  T ]
                [ 0  1 ]  used for homogeneous coordinate

        R is rotational matrix calculated from camera orination, Rz*Ry*Rx
        T is -R^-1*X ; X here is camera position in world coordinate
        '''
        for i in range(self.frame):
            posCamera = self.camera_pos[i];
            argCamera = self.camera_arg[i];

            Rz = torch.tensor(np.array([[np.cos(argCamera[2]),-np.sin(argCamera[2]),0],[np.sin(argCamera[2]),np.cos(argCamera[2]),0],[0,0,1]],dtype = np.float16));
            Ry = torch.tensor(np.array([[np.cos(argCamera[1]),0,np.sin(argCamera[1])],[0,1,0],[-np.sin(argCamera[1]),0,np.cos(argCamera[1])]],dtype = np.float16));
            Rx = torch.tensor(np.array([[1,0,0],[0,np.cos(argCamera[0]),-np.sin(argCamera[0])],[0,np.sin(argCamera[0]),np.cos(argCamera[0])]],dtype = np.float16));

            R = torch.mm(Rz,Ry);
            R = torch.mm(R,Rx);

            T = - torch.mm(R,torch.tensor(np.array(posCamera,dtype = np.float16).reshape(3,1)))

            H_ok = torch.cat((R,T),1);
            H_ok = torch.cat((H_ok,torch.tensor([[0.,0.,0.,1.]])),0);

            if i == 0:
                self.exmat = H_ok;
            elif i == 1:
                self.exmat = torch.stack((self.exmat,H_ok))
            else:
                self.exmat = torch.cat((self.exmat,H_ok.reshape(1,4,4)),0);

        self.exmat = torch.tensor(self.exmat);
        print("Extrinsic Camera Matrix generated successful!");
        return

    def inmat_generator(self):
        '''
        Generate intrinsics matrix
        * NOT COMPLETED
        '''

        self.inmat = torch.tensor(np.eye(4));

        print("Intrinsic Camera Matrix generated successful!");
        return

    def camera_transform(self,data_3d):
        """
        n: 人数;
        x: 帧数;
        data_cluster: [n,x,32,3];
        in_camera_data_cluster: 固定的内参矩阵 [3,3];
        ex_camera_data_cluster: 随帧数变化的外参矩阵 [x,3,4];
        return: [n,x,32,2];
        """
        print("Camera transform in progress")

        dataShape = data_3d.size();
        x = dataShape[0];
        n = dataShape[1];
        '''
        datasT = datas.reshape(x,n,32,4,1);
        '''
        datasInHC = torch.cat((data_3d,torch.tensor(np.ones((x,n,32,1),dtype=np.float16))),dim=3).reshape(x,n,32,4,1);
        

        datasT = torch.transpose(datasInHC,0,1);
        frame = 0;
        for data in datasT:
            data = torch.matmul(self.exmat[frame],data);
            frame += 1;
            data = torch.matmul(self.inmat,data)
        '''
        .reshape(x,n,32,3)[:,:,:,:1];;
        '''
        datasT = torch.transpose(datasT,0,1).reshape(x,n,32,4)[:,:,:,:3];
        print("Data transformed into " + str(datasT.size()))
        return datasT
        

    def update_camera(self):
        '''
        Updating the rigid-motion parameters and intrinsics parameters
        * NOT COMPLETED
        '''

        pass


