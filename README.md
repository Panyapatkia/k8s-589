# โครงงาน Kubernetes Ingress – ID 589

**รายวิชา:** CT665 Kubernetes Ingress  
**ชื่อโครงงาน:** การพัฒนาและติดตั้งระบบเว็บแอปพลิเคชันหลายบริการบน Kubernetes ด้วย NGINX Ingress Controller  
**ผู้จัดทำ:** Panyapat Sungrung  
**รหัสนักศึกษา:** 589

---

## 1. ภาพรวมโครงงาน (Project Overview)

โครงงานนี้จัดทำขึ้นเพื่อศึกษาและทดลองการติดตั้ง รวมถึงการบริหารจัดการ Web Application บนระบบ Kubernetes โดยประยุกต์ใช้ Kubernetes Deployment, Service, ConfigMap, Persistent Volume (PV), Persistent Volume Claim (PVC) และ NGINX Ingress Controller เพื่อจัดการการให้บริการแอปพลิเคชันภายใน Kubernetes Cluster

ระบบประกอบด้วย Web Application จำนวน 3 บริการ ได้แก่

1. **App About:** เว็บไซต์ส่วนตัวสำหรับแสดงหน้า Dashboard และข้อมูลแนะนำตัว
2. **App Research:** เว็บไซต์สำหรับนำเสนอข้อมูลการศึกษาและงานวิจัย พร้อมระบบจัดเก็บข้อมูลแบบ Persistent Storage
3. **App API:** เว็บแอปพลิเคชันสำหรับทดสอบการเรียกใช้งาน API ผ่าน URL Path

นอกจากนี้ยังมีการติดตั้ง External NGINX Load Balancer เพื่อรับคำขอจากผู้ใช้งานและกระจาย Traffic ไปยัง Kubernetes Worker Nodes ก่อนส่งต่อไปยัง NGINX Ingress Controller เพื่อกำหนดเส้นทางไปยังบริการต่าง ๆ ตาม Hostname และ Path ที่กำหนดไว้

### วัตถุประสงค์ของโครงงาน

1. เพื่อศึกษาและทดลองการติดตั้ง Web Application บน Kubernetes Cluster
2. เพื่อศึกษาและใช้งาน Kubernetes Deployment และ Service สำหรับบริหารจัดการแอปพลิเคชัน
3. เพื่อกำหนดเส้นทางการเข้าถึงแอปพลิเคชันผ่าน NGINX Ingress Controller
4. เพื่อศึกษาและทดลองการจัดเก็บข้อมูลแบบ Persistent Storage ด้วย PV และ PVC
5. เพื่อทดลองใช้งาน External NGINX Load Balancer สำหรับกระจายคำขอเข้าสู่ Kubernetes Cluster
6. เพื่อพัฒนาสคริปต์สำหรับช่วยติดตั้งและตรวจสอบสถานะของระบบโดยอัตโนมัติ

---

## 2. สถาปัตยกรรมระบบ (System Architecture)

### 2.1 โครงสร้าง Kubernetes Cluster

ระบบประกอบด้วย Kubernetes Cluster จำนวน 3 Nodes และ External NGINX Load Balancer จำนวน 1 เครื่อง

| Hostname | บทบาท | IP Address |
|---|---|---|
| k8s-control | Control Plane | 192.168.190.135 |
| k8s-worker1 | Worker Node 1 | 192.168.190.136 |
| k8s-worker2 | Worker Node 2 | 192.168.190.137 |
| External-LB | NGINX Load Balancer | 192.168.190.200 |

### 2.2 รายละเอียดสภาพแวดล้อม

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

### 2.3 แผนภาพสถาปัตยกรรมระบบ

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

---

## 3. รายละเอียดแอปพลิเคชัน (Application Services)

ระบบประกอบด้วยแอปพลิเคชันทั้งหมด 3 บริการ โดยติดตั้งและบริหารจัดการภายใน Namespace `id-589`

### 3.1 App About – เว็บไซต์แนะนำตัวและ Dashboard

เป็นเว็บไซต์แบบ Static Web Application พัฒนาด้วย HTML และ CSS โดยใช้ NGINX เป็น Web Server สำหรับให้บริการหน้าเว็บไซต์

ความสามารถของระบบ:
- แสดงหน้า Dashboard หลัก
- แสดงข้อมูลแนะนำตัว (About Me)
- แสดงรูปโปรไฟล์
- เชื่อมโยงไปยังบริการอื่นภายในระบบ

URL สำหรับเข้าใช้งาน:
- http://www.id-589.com/
- http://www.id-589.com/about/

### 3.2 App Research – เว็บไซต์นำเสนอข้อมูลการศึกษาและงานวิจัย

เป็น Web Application ที่พัฒนาด้วย Python Flask สำหรับนำเสนอข้อมูลการศึกษาและงานวิจัย พร้อมรองรับการจัดเก็บข้อมูลผ่าน Persistent Volume Claim

ความสามารถของระบบ:
- แสดงรายละเอียดหัวข้องานวิจัย
- แสดงแผนภาพสถาปัตยกรรมระบบ
- มีหน้าแก้ไขข้อมูลและหน้า Admin
- ใช้งาน Persistent Storage เพื่อจัดเก็บข้อมูล

URL สำหรับเข้าใช้งาน:
- http://www.id-589.com/research
- http://admin.id-589.com/edit

### 3.3 App API – บริการ API

เป็น Web Application ที่พัฒนาด้วย Python Flask สำหรับทดสอบการเรียกใช้งาน API โดยรับข้อมูลจาก URL Path และส่งผลลัพธ์กลับไปยังผู้เรียกใช้งาน

ตัวอย่าง URL:
- http://www.id-589.com/api/Hello%20Kubernetes

---

## 4. โครงสร้างไฟล์ของโครงงาน (Project Directory Structure)

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

### คำอธิบายไดเรกทอรี

| ไดเรกทอรี | รายละเอียด |
|---|---|
| `apps/` | เก็บ Source Code และไฟล์ที่ใช้พัฒนา Web Application |
| `configs/` | เก็บไฟล์ Configuration สำหรับระบบและ Load Balancer |
| `docs/` | เก็บเอกสารประกอบโครงงานและหลักฐานการทดสอบ |
| `k8s/` | เก็บ Kubernetes YAML Manifest สำหรับติดตั้ง Resource ต่าง ๆ |
| `scripts/` | เก็บ Shell Script สำหรับ Deploy และตรวจสอบระบบ |

---

## 5. สิ่งที่ต้องเตรียมก่อนติดตั้ง (Prerequisites)

ก่อนดำเนินการติดตั้งโครงงาน จำเป็นต้องเตรียมระบบและเครื่องมือดังต่อไปนี้

- Kubernetes Cluster ที่ประกอบด้วย Control Plane และ Worker Nodes
- ติดตั้งและกำหนดค่า `kubectl` ให้สามารถเชื่อมต่อ Kubernetes Cluster ได้
- ติดตั้ง Container Runtime โดยใช้ containerd
- ติดตั้ง Flannel CNI สำหรับการสื่อสารระหว่าง Kubernetes Nodes
- ติดตั้ง NGINX Ingress Controller
- ติดตั้งและกำหนดค่า External NGINX Load Balancer
- เตรียม Container Images ที่จำเป็นสำหรับแต่ละ Application ให้พร้อมใช้งานบน Kubernetes Nodes

---

## 6. ขั้นตอนการติดตั้งและ Deploy ระบบ (Installation and Deployment)

### 6.1 ดาวน์โหลด Source Code

ดำเนินการ Clone Repository จาก GitHub

```bash
git clone https://github.com/Panyapatkia/k8s-589.git

cd k8s-589
```

### 6.2 กำหนดค่า Hostname Resolution

กำหนดค่า Hostname บนเครื่อง Client หรือ DNS Server เพื่อให้สามารถเรียกใช้งานเว็บไซต์ผ่าน Domain Name ได้

ตัวอย่างการกำหนดค่าในไฟล์ `/etc/hosts`

```text
192.168.190.200 www.id-589.com
192.168.190.200 admin.id-589.com
```

### 6.3 กำหนดค่า External NGINX Load Balancer

กำหนดค่า External NGINX Load Balancer เพื่อรับคำขอจากผู้ใช้งานและส่งต่อไปยัง NGINX Ingress Controller ผ่าน NodePort ของ Kubernetes Worker Nodes

ไฟล์ Configuration:

```text
configs/k8s-lb.conf
```

กำหนด HTTP NodePort เป็น `31080`

### 6.4 ดำเนินการ Deploy Kubernetes Resources

กำหนดสิทธิ์การทำงานให้กับ Shell Script

```bash
chmod +x scripts/deploy.sh
chmod +x scripts/verify.sh
```

เรียกใช้งาน Deployment Script

```bash
./scripts/deploy.sh
```

สคริปต์จะดำเนินการติดตั้ง Resource ตามลำดับดังนี้

1. สร้าง Namespace
2. ติดตั้ง Storage Resources
3. ติดตั้ง ConfigMap สำหรับ App About
4. Deploy App About และ Service
5. Deploy App Research และ Service
6. Deploy App API และ Service
7. ติดตั้ง Ingress Resource
8. ตรวจสอบสถานะของ Resource ภายใน Kubernetes Cluster

---

## 7. การตรวจสอบระบบ (System Verification)

หลังจากดำเนินการ Deploy เรียบร้อยแล้ว สามารถตรวจสอบสถานะของระบบได้ด้วยคำสั่งต่อไปนี้

### 7.1 ตรวจสอบสถานะ Kubernetes Nodes

```bash
kubectl get nodes -o wide
```

### 7.2 ตรวจสอบ Deployment และ Pods

```bash
kubectl get deployments,pods -n id-589 -o wide
```

### 7.3 ตรวจสอบ Services

```bash
kubectl get svc -n id-589
```

### 7.4 ตรวจสอบ Persistent Storage

```bash
kubectl get pv,pvc -n id-589
```

### 7.5 ตรวจสอบ Ingress

```bash
kubectl get ingress -n id-589
```

### 7.6 เรียกใช้งาน Verification Script

```bash
./scripts/verify.sh
```

### 7.7 ทดสอบการเข้าถึงเว็บไซต์ผ่าน Load Balancer

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

---

## 8. สรุป URL สำหรับเข้าใช้งานระบบ (Application Access)

| บริการ | URL | รายละเอียด |
|---|---|---|
| Dashboard | http://www.id-589.com/ | หน้า Dashboard หลัก |
| About Me | http://www.id-589.com/about/ | หน้าแนะนำตัว |
| Research | http://www.id-589.com/research | หน้านำเสนอข้อมูลการศึกษาและงานวิจัย |
| API | http://www.id-589.com/api/Hello%20Kubernetes | ทดสอบเรียกใช้งาน API |
| Admin | http://admin.id-589.com/edit | หน้า Admin สำหรับจัดการข้อมูล Research |

---

## 9. การแก้ไขปัญหาเบื้องต้น (Troubleshooting)

### 9.1 ตรวจสอบสถานะ Pods

```bash
kubectl get pods -n id-589 -o wide
```

### 9.2 ตรวจสอบรายละเอียด Pod

```bash
kubectl describe pod <POD_NAME> -n id-589
```

### 9.3 ตรวจสอบ Application Logs

```bash
kubectl logs <POD_NAME> -n id-589
```

### 9.4 ตรวจสอบ NGINX Ingress Controller

```bash
kubectl get pods -n ingress-nginx
```

### 9.5 ตรวจสอบ Ingress Configuration

```bash
kubectl describe ingress app-ingress -n id-589
```

### 9.6 Restart Application Deployment

ตัวอย่างการ Restart App About

```bash
kubectl rollout restart deployment/app-about -n id-589
```

---

## 10. การลบระบบ (Cleanup)

หากต้องการลบ Resource ของโครงงานออกจาก Kubernetes Cluster สามารถใช้คำสั่ง

```bash
kubectl delete namespace id-589
```

**หมายเหตุ:** การลบ Namespace จะทำให้ Resource ทั้งหมดภายใน Namespace ถูกลบ รวมถึง PVC ที่เกี่ยวข้อง ควรสำรองข้อมูลสำคัญก่อนดำเนินการ และตรวจสอบ Reclaim Policy ของ PV ก่อนทุกครั้ง

---

## 11. GitHub Repository

Source Code และไฟล์ Configuration ของโครงงานสามารถเข้าถึงได้จาก GitHub Repository

**Repository:**  
https://github.com/Panyapatkia/k8s-589

---

## 12. ผู้จัดทำ (Project Author)

**ชื่อ:** Panyapat Sungrung  
**รหัสนักศึกษา:** 589  
**รายวิชา:** CT665 Kubernetes Ingress
