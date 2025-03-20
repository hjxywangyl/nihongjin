-- 创建日语词汇表
CREATE TABLE IF NOT EXISTS public.japanese_vocabulary (
    id SERIAL PRIMARY KEY,
    expression TEXT NOT NULL,  -- 汉字表达
    reading TEXT NOT NULL,     -- 假名读音
    meaning TEXT,             -- 中文含义
    example TEXT,             -- 例句
    jlpt_level INTEGER,       -- JLPT等级
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- 创建剧本表
CREATE TABLE IF NOT EXISTS public.drama_scripts (
    id SERIAL PRIMARY KEY,
    drama_title TEXT NOT NULL,    -- 剧集名称
    episode INTEGER NOT NULL,     -- 集数
    character TEXT NOT NULL,      -- 角色名称
    content TEXT NOT NULL,        -- 对话内容
    content_furigana TEXT,        -- 带注音的对话内容
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_japanese_vocabulary_reading ON public.japanese_vocabulary(reading);
CREATE INDEX IF NOT EXISTS idx_japanese_vocabulary_expression ON public.japanese_vocabulary(expression);
CREATE INDEX IF NOT EXISTS idx_drama_scripts_content ON public.drama_scripts(content);
CREATE INDEX IF NOT EXISTS idx_drama_scripts_content_furigana ON public.drama_scripts(content_furigana);
CREATE INDEX IF NOT EXISTS idx_drama_scripts_drama_title ON public.drama_scripts(drama_title);

-- 插入一些示例数据
INSERT INTO public.japanese_vocabulary (expression, reading, meaning, example, jlpt_level) VALUES
('私', 'わたし', '我', '私は学生です。', 5),
('学生', 'がくせい', '学生', '私は学生です。', 5),
('です', 'です', '是（礼貌语）', '私は学生です。', 5),
('食べる', 'たべる', '吃', 'ご飯を食べます。', 5),
('ご飯', 'ごはん', '米饭，饭', 'ご飯を食べます。', 5);

INSERT INTO public.drama_scripts (drama_title, episode, character, content, content_furigana) VALUES
('サンプルドラマ', 1, '山田太郎', 'こんにちは、私は山田です。', 'こんにちは、わたしはやまだです。'),
('サンプルドラマ', 1, '鈴木花子', 'はじめまして、鈴木です。', 'はじめまして、すずきです。'); 