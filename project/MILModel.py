"""
@author: Radosław Pławecki
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class MILModelK5(nn.Module):
    def __init__(self, input_dim=256, hidden_dim=128, dropout=0.2):
        super().__init__()
        self.encoder = nn.Linear(input_dim, hidden_dim)
        self.dropout = nn.Dropout(dropout)
        
        self.attention = nn.Sequential(
            nn.Linear(hidden_dim, 64),
            nn.Tanh(),
            nn.Linear(64, 1)
        )
        self.classifier = nn.Linear(hidden_dim, 1)
        self.bn = nn.BatchNorm1d(hidden_dim)
        
    def forward(self, bag):
        H = self.encoder(bag)              # [liczba_kontigów, hidden_dim]
        H = self.dropout(H)                # regularizacja
        A = torch.softmax(self.attention(H), dim=0)
        M = torch.sum(A * H, dim=0)
        M = self.bn(M.unsqueeze(0)).squeeze(0)
        out = torch.sigmoid(self.classifier(M))
        return out, A
    