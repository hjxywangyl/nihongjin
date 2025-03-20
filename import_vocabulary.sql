-- 创建临时表来存储CSV数据
CREATE TEMP TABLE temp_vocabulary (
    expression TEXT,
    reading TEXT,
    meaning TEXT,
    tags TEXT,
    guid TEXT
);

-- 从CSV文件导入数据到临时表
COPY temp_vocabulary FROM STDIN WITH (FORMAT csv, HEADER true);

-- 插入数据到主表，处理tags字段
INSERT INTO public.japanese_vocabulary (expression, reading, meaning, jlpt_level)
SELECT 
    expression,
    reading,
    meaning,
    CASE 
        WHEN tags LIKE '%JLPT_N1%' THEN 1
        WHEN tags LIKE '%JLPT_N2%' THEN 2
        WHEN tags LIKE '%JLPT_N3%' THEN 3
        WHEN tags LIKE '%JLPT_N4%' THEN 4
        WHEN tags LIKE '%JLPT_N5%' THEN 5
        ELSE NULL
    END as jlpt_level
FROM temp_vocabulary
WHERE expression IS NOT NULL 
AND reading IS NOT NULL;

-- 删除临时表
DROP TABLE temp_vocabulary; 