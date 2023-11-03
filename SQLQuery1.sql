CREATE DATABASE My_Projects

use My_Projects

CREATE TABLE MEGA_SENA(
	ID INT PRIMARY KEY IDENTITY,
	CONCURSO VARCHAR(30) NOT NULL,
	DATA_CONCURSO DATE NULL,
	APOSTA VARCHAR(50) NOT NULL,
	VENCEDOR VARCHAR(30) NOT NULL

)
drop table MEGA_SENA

select * from MEGA_SENA

select concurso,data_concurso,aposta,vencedor 
from MEGA_SENA
where vencedor = 'Ganhadora'
order by vencedor


SELECT Aposta AS Numero, COUNT(*) AS Frequencia
FROM MEGA_SENA
GROUP BY Aposta
ORDER BY Frequencia DESC;
