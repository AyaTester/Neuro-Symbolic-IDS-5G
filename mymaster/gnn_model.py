
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from graph_to_pyg import data, all_nodes 
class SecurityGNN(torch.nn.Module):
    def __init__(self, num_node_features, num_classes):
        super(SecurityGNN, self).__init__()
        self.conv1 = GCNConv(num_node_features, 32) # رفعنا السعة لـ 32
        self.conv2 = GCNConv(32, 16)               # طبقة وسيطة
        self.conv3 = GCNConv(16, num_classes)      # طبقة المخرجات

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p=0.2, training=self.training)
        x = self.conv2(x, edge_index)
        x = F.relu(x)
        x = self.conv3(x, edge_index)
        return F.log_softmax(x, dim=1)
    

# إعداد الموديل
# num_node_features هو عدد العقد (27) في حالتنا الحالية لأننا استخدمنا Identity Matrix
# بدلاً من 27، سنستخدم 3 ميزات كمدخلات
model = SecurityGNN(num_node_features=data.num_node_features, num_classes=2)
print(model)