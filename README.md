## Một số chỉnh sửa trong schema

-- User có thêm trường phone

## Sử dụng

----Em có tạo sẵn 1 user và 2 products trong data_sample.py, nếu muốn test api:
chạy trong integrated terminal bằng lệnh:

    uvicorn data_sample:app            <lưu ý không có --reload>

----Sau khi có data có thể test api như bình thường được rồi

    uvicorn main:app --reload

## Lưu ý

----Trong các phần import của main(line 7) và của routes.py (line 5), cần xóa web_mission
----đi nếu như chỉ pull về thay vì clone
