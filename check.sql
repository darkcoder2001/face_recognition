use face_recognition
select*from attention_manager
select*from user_manager

use face_recognition
select*from user_manager
select*from attention_manager
select*from job_position

SELECT CheckInTime, CheckOutTime
FROM attention_manager
WHERE UserID = 1 AND AttentionDate = CAST(GETDATE() AS DATE)

delete from attention_manager
where AttentionDate='2024-11-27'

UPDATE attention_manager
SET Status = 'Muon'
WHERE month(AttentionDate) = '08'