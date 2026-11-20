
from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path

app = Flask(__name__)

DATA_DIR = Path("/data")
DATA_FILE = DATA_DIR / "research.txt"

DEFAULT_RESEARCH = """งานวิจัยนี้มีที่มาและความสำคัญจากการเติบโตของเทคโนโลยี Cloud Computing, Big Data และ Artificial Intelligence ซึ่งส่งผลให้ปริมาณข้อมูลที่ต้องจัดเก็บเพิ่มขึ้นอย่างต่อเนื่อง ระบบ Object Storage จึงเป็นเทคโนโลยีสำคัญสำหรับการจัดเก็บข้อมูลจำนวนมาก โดยรองรับการเข้าถึงข้อมูลผ่าน S3-compatible API อย่างไรก็ตาม ประสิทธิภาพของระบบอาจได้รับผลกระทบจากรูปแบบการจัดการพื้นที่จัดเก็บข้อมูลที่แตกต่างกัน

การวิจัยนี้มีวัตถุประสงค์เพื่อศึกษาและเปรียบเทียบประสิทธิภาพของระบบ Object Storage จำนวน 3 ระบบ ได้แก่ MinIO, SeaweedFS และ RustFS ภายใต้รูปแบบการจัดการพื้นที่จัดเก็บข้อมูล 2 รูปแบบ คือ Separate Disk (JBOD) และ LVM Striped Pool เพื่อศึกษาพฤติกรรมการทำงานของระบบภายใต้เงื่อนไขการจัดเก็บข้อมูลที่แตกต่างกัน

การออกแบบการทดลองดำเนินการบนสภาพแวดล้อมเสมือน VMware ESXi โดยกำหนดสภาพแวดล้อมการทดลองทั้งหมด 6 รูปแบบ จากระบบ Object Storage 3 ระบบ และ Storage Layout 2 รูปแบบ แต่ละสภาพแวดล้อมประกอบด้วย Virtual Machine จำนวน 4 เครื่อง รวมทั้งสิ้น 24 Virtual Machines โดยควบคุมทรัพยากร ระบบปฏิบัติการ และเครือข่ายให้มีเงื่อนไขสอดคล้องกัน พร้อมใช้ HAProxy สำหรับกระจายคำขอไปยังโหนดของระบบ

การทดสอบประสิทธิภาพใช้เครื่องมือ MinIO WARP สร้างภาระงานในรูปแบบ PUT และ GET โดยกำหนดขนาดออบเจ็กต์ 3 ขนาด ได้แก่ 4 KiB, 16 MiB และ 256 MiB กำหนด Concurrency เท่ากับ 4 ระยะเวลาทดสอบ 5 นาทีต่อรอบ และทดสอบซ้ำ 5 รอบต่อกรณีทดสอบ รวมทั้งสิ้น 180 รอบการทดสอบ

การศึกษามุ่งเน้นการเปรียบเทียบอัตราการรับส่งข้อมูล (Throughput) ระยะเวลาตอบสนอง (Latency) และการใช้ทรัพยากรของระบบ เพื่อวิเคราะห์พฤติกรรมและความแตกต่างของระบบ Object Storage แต่ละประเภทภายใต้รูปแบบการจัดการพื้นที่จัดเก็บข้อมูลที่กำหนด โดยใช้กระบวนการทดลองที่ควบคุมเงื่อนไขให้สามารถเปรียบเทียบกันได้อย่างเป็นระบบ
"""


def read_research():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        DATA_FILE.write_text(DEFAULT_RESEARCH, encoding="utf-8")

    return DATA_FILE.read_text(encoding="utf-8")


@app.route("/")
@app.route("/research")
def research():
    content = read_research()
    return render_template("research.html", content=content)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        content = request.form.get("content", "")
        DATA_FILE.write_text(content, encoding="utf-8")
        return redirect("http://www.id-589.com/research")

    return render_template("edit.html", content=read_research())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

