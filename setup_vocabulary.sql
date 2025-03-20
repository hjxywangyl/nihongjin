-- 如果表存在，先删除它
DROP TABLE IF EXISTS public.japanese_vocabulary;

-- 创建日语词汇表
CREATE TABLE public.japanese_vocabulary (
    id SERIAL PRIMARY KEY,
    expression TEXT NOT NULL,  -- 汉字表达
    reading TEXT NOT NULL,     -- 假名读音
    meaning TEXT,             -- 中文含义
    example TEXT,             -- 例句
    jlpt_level INTEGER,       -- JLPT等级
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- 创建索引以提高查询性能
CREATE INDEX idx_japanese_vocabulary_reading ON public.japanese_vocabulary(reading);
CREATE INDEX idx_japanese_vocabulary_expression ON public.japanese_vocabulary(expression);

-- 插入示例数据
INSERT INTO public.japanese_vocabulary (expression, reading, meaning, example, jlpt_level) VALUES
('私', 'わたし', '我', '私は学生です。', 5),
('学生', 'がくせい', '学生', '私は学生です。', 5),
('です', 'です', '是（礼貌语）', '私は学生です。', 5),
('食べる', 'たべる', '吃', 'ご飯を食べます。', 5),
('ご飯', 'ごはん', '米饭，饭', 'ご飯を食べます。', 5),
('山田', 'やまだ', '山田（姓氏）', '山田さんは学生です。', 5),
('鈴木', 'すずき', '铃木（姓氏）', '鈴木さんは先生です。', 5),
('先生', 'せんせい', '老师', '鈴木さんは先生です。', 5),
('こんにちは', 'こんにちは', '你好', 'こんにちは、私は山田です。', 5),
('はじめまして', 'はじめまして', '初次见面', 'はじめまして、鈴木です。', 5); 