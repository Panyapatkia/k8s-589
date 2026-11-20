# Kubernetes Multi-Service & Ingress Project (ID: 68130589)

**รายวิชา:** CT665 Kubernetes
**ผู้จัดทำ:** Panyapat Sungrung (รหัสนักศึกษา: `68130589`)  
**โดเมนที่ให้บริการ:** `www.id-589.com` และ `admin.id-589.com`
---

## 1. สถาปัตยกรรมระบบ (Architecture)

ระบบประกอบด้วย Kubernetes Cluster จำนวน 3 Nodes และ External NGINX Load Balancer จำนวน 1 เครื่อง ทำหน้าที่รับคำขอจากผู้ใช้งานและส่งต่อไปยัง NGINX Ingress Controller เพื่อกำหนดเส้นทางไปยัง Web Application แต่ละบริการตาม Domain Name และ URL Path ที่กำหนดไว้

### โครงสร้าง Kubernetes Cluster

| Hostname | บทบาท | IP Address |
|---|---|---|
| k8s-control | Control Plane | 192.168.190.135 |
| k8s-worker1 | Worker Node 1 | 192.168.190.136 |
| k8s-worker2 | Worker Node 2 | 192.168.190.137 |
| External-LB | NGINX Load Balancer | 192.168.190.200 |

### รายละเอียดสภาพแวดล้อม

| รายการ | รายละเอียด |
|---|---|
| Operating System | Ubuntu 24.04.4 LTS |
| Kubernetes Version | v1.37.1 |
| Container Runtime | containerd 2.2.1 |
| CNI Plugin | Flannel |
| Ingress Controller | NGINX Ingress Controller |
| HTTP NodePort | 31080 |
| HTTPS NodePort | 31502 |
| Kubernetes Namespace | id-589 |

### แผนภาพสถาปัตยกรรมระบบ

```text
                  Users / Web Browser
                          |
                          |
               External NGINX Load Balancer
                   192.168.190.200
                          |
                -------------------------
                |                       |
           Worker Node 1           Worker Node 2
           192.168.190.136         192.168.190.137
                |                       |
                +-----------+-----------+
                            |
                  NGINX Ingress Controller
                     NodePort : 31080
                            |
                       app-ingress
                            |
                  Kubernetes Services
                            |
               +------------+------------+
               |            |            |
            svc-about   svc-research   svc-api
               |            |            |
            App About   App Research   App API
            Deployment  Deployment    Deployment
               |            |            |
            NGINX Pods   Flask Pods    Flask Pods
                            |
                       PVC / PV
```

### การกำหนดเส้นทางการเข้าใช้งาน (Ingress Routing)

| Domain | URL Path | ปลายทาง | รายละเอียด |
|---|---|---|---|
| www.id-589.com | `/` | svc-about | หน้า Dashboard |
| www.id-589.com | `/about/` | svc-about | หน้า About Me |
| www.id-589.com | `/research` | svc-research | เว็บไซต์ Research |
| www.id-589.com | `/api/Hello%20Kubernetes` | svc-api | บริการ API |
| admin.id-589.com | `/edit` | svc-research | หน้า Admin |

---

## 2. โครงสร้างไฟล์ใน Repository

```text
k8s-589/
├── apps/
│   ├── app-about/
│   │   ├── about/
│   │   │   ├── index.html
│   │   │   └── profile.png
│   │   ├── Containerfile
│   │   └── index.html
│   │
│   ├── app-api/
│   │   ├── app.py
│   │   ├── Containerfile
│   │   ├── requirements.txt
│   │   └── templates/
│   │       └── index.html
│   │
│   └── app-research/
│       ├── app.py
│       ├── Containerfile
│       ├── requirements.txt
│       ├── static/
│       │   └── research-architecture.png
│       └── templates/
│           ├── edit.html
│           └── research.html
│
├── configs/
│   ├── etc-hosts-linux.txt
│   └── k8s-lb.conf
│
├── docs/
│
├── k8s/
│   ├── 00-namespace.yaml
│   ├── 01-storage.yaml
│   ├── 02-app-about-configmap.yaml
│   ├── 02-app-about-deployment.yaml
│   ├── 03-app-research.yaml
│   ├── 04-app-api.yaml
│   └── 05-ingress.yaml
│
├── scripts/
│   ├── deploy.sh
│   └── verify.sh
│
├── .gitignore
└── README.md
```

### คำอธิบายไฟล์และไดเรกทอรี

| ไดเรกทอรี / ไฟล์ | รายละเอียด |
|---|---|
| `apps/` | เก็บ Source Code และไฟล์ที่ใช้พัฒนา Web Application ทั้ง 3 บริการ |
| `apps/app-about/` | เว็บไซต์ Dashboard และหน้าแนะนำตัว |
| `apps/app-api/` | Source Code สำหรับให้บริการ API ด้วย Python Flask |
| `apps/app-research/` | Source Code สำหรับเว็บไซต์ Research ด้วย Python Flask |
| `configs/` | เก็บไฟล์ Configuration สำหรับ Hostname และ External NGINX Load Balancer |
| `docs/` | เก็บเอกสารประกอบโครงงานและหลักฐานการทดสอบ |
| `k8s/` | เก็บ Kubernetes YAML Manifest สำหรับสร้างและบริหารจัดการ Resource |
| `scripts/` | เก็บ Shell Script สำหรับ Deploy และตรวจสอบระบบ |
| `README.md` | เอกสารแนะนำโครงงานและขั้นตอนการใช้งาน |

---

## 3. ขั้นตอนการ Deploy ตั้งแต่ต้นจนใช้งานได้

> **หมายเหตุ:** ก่อนเริ่มต้นต้องเตรียม Kubernetes Cluster ให้พร้อมใช้งาน รวมถึงติดตั้ง Flannel CNI และ NGINX Ingress Controller ให้เรียบร้อย เนื่องจาก `deploy.sh` ของโครงงานนี้ทำหน้าที่ Deploy Application Resources ไม่ได้ติดตั้ง Kubernetes Cluster หรือ Ingress Controller ให้อัตโนมัติ

### ขั้นตอนที่ 1: ดาวน์โหลด Source Code จาก GitHub

ดำเนินการ Clone Repository บนเครื่อง `k8s-control`

```bash
git clone https://github.com/Panyapatkia/k8s-589.git

cd k8s-589
```

### ขั้นตอนที่ 2: เตรียมระบบและตรวจสอบ Kubernetes Cluster

ตรวจสอบสถานะ Kubernetes Nodes

```bash
kubectl get nodes -o wide
```

ตรวจสอบ NGINX Ingress Controller

```bash
kubectl get pods -n ingress-nginx
```

ตรวจสอบ Flannel CNI

```bash
kubectl get pods -n kube-flannel
```

กำหนดสิทธิ์การทำงานให้กับ Shell Script

```bash
chmod +x scripts/deploy.sh
chmod +x scripts/verify.sh
```

### ขั้นตอนที่ 3: Deploy Kubernetes Resources

ดำเนินการติดตั้ง Application และ Kubernetes Resources ด้วย Deployment Script

```bash
./scripts/deploy.sh
```

สคริปต์จะดำเนินการตามลำดับดังนี้

1. สร้าง Namespace `id-589`
2. ติดตั้ง Storage Resources
3. ติดตั้ง ConfigMap สำหรับ App About
4. Deploy App About และ Service
5. Deploy App Research และ Service
6. Deploy App API และ Service
7. ติดตั้ง Ingress Resource
8. ตรวจสอบสถานะของ Kubernetes Resources

### ขั้นตอนที่ 4: กำหนดค่า External NGINX Load Balancer

นำไฟล์ Configuration จาก Repository

```text
configs/k8s-lb.conf
```

ไปติดตั้งบนเครื่อง `External-LB` ที่มี IP Address `192.168.190.200` โดยกำหนดให้ NGINX รับคำขอจากผู้ใช้งานผ่าน HTTP Port 80 และส่งต่อไปยัง Kubernetes Worker Nodes ผ่าน NodePort `31080`

หลังจากติดตั้งไฟล์ Configuration ให้ตรวจสอบและ Reload NGINX

```bash
sudo nginx -t
sudo systemctl reload nginx
```

### ขั้นตอนที่ 5: กำหนดค่า Hostname Resolution

กำหนดค่า Hostname บนเครื่อง Client เพื่อให้สามารถเรียกใช้งานเว็บไซต์ผ่าน Domain Name ได้

**บน Linux:** แก้ไขไฟล์ `/etc/hosts`

```text
192.168.190.200 www.id-589.com admin.id-589.com
```

**บน Windows:** แก้ไขไฟล์

```text
C:\Windows\System32\drivers\etc\hosts
```

เพิ่มรายการดังนี้

```text
192.168.190.200 www.id-589.com admin.id-589.com
```

### ขั้นตอนที่ 6: ทดสอบการเข้าใช้งานเว็บไซต์

เปิด Web Browser และทดสอบเข้าใช้งานผ่าน Domain Name ที่กำหนดไว้

- `http://www.id-589.com/`
- `http://www.id-589.com/about/`
- `http://www.id-589.com/research`
- `http://www.id-589.com/api/Hello%20Kubernetes`
- `http://admin.id-589.com/edit`

---

## 4. การตรวจสอบการทำงาน (Verification)

ดำเนินการตรวจสอบสถานะของระบบหลังจาก Deploy เรียบร้อยแล้ว โดยสามารถใช้คำสั่งต่อไปนี้บนเครื่อง `k8s-control`

### ตรวจสอบสถานะ Kubernetes Nodes

```bash
kubectl get nodes -o wide
```

### ตรวจสอบ Deployment และ Pods

```bash
kubectl get deployments,pods -n id-589 -o wide
```

### ตรวจสอบ Services

```bash
kubectl get svc -n id-589
```

### ตรวจสอบ Persistent Storage

```bash
kubectl get pv,pvc -n id-589
```

### ตรวจสอบ Ingress

```bash
kubectl get ingress -n id-589
```

### ตรวจสอบสถานะ Application ด้วย Script

```bash
bash scripts/verify.sh
```

### ทดสอบ HTTP ผ่าน External Load Balancer

ทดสอบหน้า Dashboard

```bash
curl -I -H "Host: www.id-589.com" \
http://192.168.190.200/
```

ทดสอบหน้า Research

```bash
curl -I -H "Host: www.id-589.com" \
http://192.168.190.200/research
```

ทดสอบหน้า Admin

```bash
curl -I -H "Host: admin.id-589.com" \
http://192.168.190.200/edit
```

---

**GitHub Repository:**  
https://github.com/Panyapatkia/k8s-589

**ผู้จัดทำ:** Panyapat Sungrung  
**รหัสนักศึกษา:** 68130589  
**รายวิชา:** CT665 Kubernetes Ingress
