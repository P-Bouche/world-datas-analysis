--------------------------------------
-- Export
--------------------------------------

.head on
.nullvalue NULL
.mode csv
.output global/covid-19/datas/global_covid19_JHU_export.csv
select * from v_global_covid19_JHU;
