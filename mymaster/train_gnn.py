import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from neo4j import GraphDatabase
import numpy as np

# 1. تعريف بنية الموديل (Neuro Layer)
class SecurityGNN(torch.nn.Module):
    def __init__(self, hidden_channels):
        super(SecurityGNN, self).__init__()
        # 11 ميزة (10 من CSV + 1 ميزة الـ Degree التي أضفناها)
        self.conv1 = GCNConv(11, 64) 
        self.conv2 = GCNConv(64, 32)
        self.conv3 = GCNConv(32, 2)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = F.relu(self.conv1(x, edge_index))
        x = F.dropout(x, p=0.3, training=self.training)
        x = F.relu(self.conv2(x, edge_index))
        x = self.conv3(x, edge_index)
        return x

# 2. دالة التدريب مع Gradient Clipping لضمان الاستقرار
def train(model, data, optimizer, criterion):
    model.train()
    optimizer.zero_grad()
    out = model(data)
    loss = criterion(out[data.train_mask], data.y[data.train_mask])
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    optimizer.step()
    return loss

# 3. دالة الاختبار
def test(model, data):
    model.eval()
    out = model(data)
    pred = out.argmax(dim=1)
    correct = (pred[data.test_mask] == data.y[data.test_mask]).sum()
    acc = int(correct) / int(data.test_mask.sum())
    return acc, pred

# 4. دالة التصدير للطبقة الرمزية (Symbolic Injection)
def export_to_symbolic_layer(all_ips, predictions):
    uri = "bolt://localhost:7687"
    driver = GraphDatabase.driver(uri, auth=("neo4j","Asdfqwer@1234#")) # تأكدي من كلمة المرور
    with driver.session() as session:
        print("--- جاري حقن النتائج في الطبقة الرمزية (Neo4j) ---")
        for ip, pred in zip(all_ips, predictions):
            status = "Attack" if pred == 1 else "Normal"
            session.run("MATCH (n:IP {address: $ip}) SET n.status = $status", 
                        ip=ip, status=status)
    driver.close()

# 5. الإعدادات والتشغيل الرئيسي
if __name__ == "__main__":
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # تحميل البيانات (تأكدي من وجود weights_only=False للنسخ الحديثة)
    data = torch.load('data.pt', weights_only=False).to(device)
    
    model = SecurityGNN(hidden_channels=64).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0005, weight_decay=5e-4)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=20, factor=0.5)
    criterion = torch.nn.CrossEntropyLoss(weight=torch.tensor([2.0, 1.0]).to(device))

    best_acc = 0
    print("--- بدء تدريب الموديل المستقر (Aya's Neuro-Symbolic IDS) ---")

    for epoch in range(1, 301):
        loss = train(model, data, optimizer, criterion)
        test_acc, current_preds = test(model, data)
        scheduler.step(loss.detach())
        
        if test_acc > best_acc:
            best_acc = test_acc
            torch.save(model.state_dict(), 'best_model.pth')
            final_predictions = current_preds.cpu().numpy()
          
        if epoch % 50 == 0:
            print(f'Epoch: {epoch:03d}, Loss: {loss:.4f}, Best Acc: {best_acc:.4f}')
        # تعديل آلية الحفظ لتسمية الموديل حسب نوع التجربة
        if test_acc > best_acc:
             best_acc = test_acc
    torch.save(model.state_dict(), 'gnn_iot_expert.pth') # حفظ نسخة خبيرة
    print(f"--- انتهى التدريب. أعلى دقة: {best_acc:.4f} ---")

    # الربط الرمزي باستخدام أسماء الـ IPs المخزنة في البيانات
    if hasattr(data, 'node_names'):
        export_to_symbolic_layer(data.node_names, final_predictions)
        print("--- تم تفعيل الجانب الرمزي بنجاح ---")
    else:
        print("⚠️ تحذير: لم يتم العثور على أسماء العقد (IPs) في ملف data.pt")

import time
start_time = time.time()
out = model(data) # عملية الاستنتاج
end_time = time.time()
print(f"Inference Time: {end_time - start_time:.4f} seconds")