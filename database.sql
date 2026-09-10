-- Галамарт Склад — Проектирование БД Р2.3
-- 7 таблиц, 3НФ (добавлена users для входа)
-- СУБД: SQLite / MySQL совместимый

PRAGMA foreign_keys = ON;

-- 1. Категории
CREATE TABLE categories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE
);

-- 2. Поставщики
CREATE TABLE suppliers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  contact TEXT,
  phone TEXT,
  created_at TEXT DEFAULT (datetime('now'))
);

-- 3. Товары (сущность)
CREATE TABLE products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sku TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  category_id INTEGER NOT NULL REFERENCES categories(id),
  supplier_id INTEGER NOT NULL REFERENCES suppliers(id),
  unit TEXT NOT NULL DEFAULT 'шт',
  location TEXT, -- ячейка A-01-02
  min_stock INTEGER NOT NULL CHECK (min_stock >= 1),
  price REAL NOT NULL CHECK (price >= 0),
  created_at TEXT DEFAULT (datetime('now'))
);

-- 4. Склад (остатки) — вынесено для 3НФ (отдельно от справочника товара)
CREATE TABLE stock (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id INTEGER NOT NULL UNIQUE REFERENCES products(id) ON DELETE CASCADE,
  quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
  updated_at TEXT DEFAULT (datetime('now'))
);

-- 5. Заявки
CREATE TABLE orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  supplier_id INTEGER NOT NULL REFERENCES suppliers(id),
  status TEXT NOT NULL CHECK (status IN ('new','sent','received')),
  comment TEXT,
  created_at TEXT NOT NULL DEFAULT (date('now'))
);

-- 6. Позиции заявки (M:N)
CREATE TABLE order_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  product_id INTEGER NOT NULL REFERENCES products(id),
  qty INTEGER NOT NULL CHECK (qty >= 1),
  price REAL NOT NULL CHECK (price >= 0),
  UNIQUE(order_id, product_id)
);

-- 7. Пользователи (вход + админ-панель)
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  login TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL, -- в демо plain, в проде bcrypt
  name TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin','director','manager')),
  status TEXT NOT NULL CHECK (status IN ('pending','approved','rejected')),
  created_at TEXT DEFAULT (datetime('now'))
);

-- Индексы
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_stock_product ON stock(product_id);
CREATE INDEX idx_orders_supplier ON orders(supplier_id);
CREATE INDEX idx_orders_status ON orders(status);

-- Seed
INSERT INTO categories(name) VALUES ('Посуда'),('Текстиль'),('Бытовая химия'),('Хозтовары'),('Инструменты'),('Декор');

INSERT INTO suppliers(name, contact) VALUES
 ('ООО «Поставщик-1» — Посуда Оптом','opt@posuda.ru'),
 ('ИП Текстиль Снаб','textil@sibmail.ru'),
 ('ООО «ХимТорг»','him@torg.ru'),
 ('ООО «Инструмент Сибирь»','instr@sib.ru');

INSERT INTO products(sku,name,category_id,supplier_id,unit,location,min_stock,price) VALUES
 ('GLM-101','Набор кастрюль 6 пр. нерж.',1,1,'шт','A-01-02',10,4590),
 ('GLM-102','Сковорода антипригарная 28см',1,1,'шт','A-01-05',12,1890),
 ('GLM-103','Полотенце махровое 70x140',2,2,'шт','B-02-01',15,890),
 ('GLM-104','Плед флисовый 150x200',2,2,'шт','B-02-04',10,1290),
 ('GLM-105','Средство для посуды 1л',3,3,'шт','C-03-01',20,320),
 ('GLM-106','Салфетки микрофибра 3шт',3,3,'уп','C-03-03',15,450),
 ('GLM-107','Набор контейнеров 5шт',4,1,'набор','A-04-02',12,990),
 ('GLM-108','Вешалки 10шт металл',4,2,'уп','B-04-01',10,590),
 ('GLM-109','Набор отвёрток 6шт',5,4,'набор','D-05-02',8,1490),
 ('GLM-110','Молоток 500г',5,4,'шт','D-05-04',8,790),
 ('GLM-111','Ваза керамика 25см',6,1,'шт','E-06-01',6,1190),
 ('GLM-112','Свечи ароматические 6шт',6,1,'уп','E-06-03',12,690),
 ('GLM-113','Швабра с отжимом',4,3,'шт','C-04-05',10,1390),
 ('GLM-114','Порошок стиральный 3кг',3,3,'шт','C-03-07',15,890);

INSERT INTO stock(product_id, quantity) VALUES
 (1,4),(2,18),(3,5),(4,22),(5,2),(6,35),(7,9),(8,27),(9,6),(10,14),(11,3),(12,40),(13,8),(14,11);

INSERT INTO orders(supplier_id,status,comment,created_at) VALUES (3,'sent','Срочно', '2026-06-20'), (1,'new','Пополнение','2026-06-22');
INSERT INTO order_items(order_id,product_id,qty,price) VALUES (1,5,18,320),(1,14,10,890),(2,1,8,4590);

INSERT INTO users(login,password_hash,name,role,status) VALUES
 ('admin','123','Администратор','admin','approved'),
 ('manager','manager123','Товаровед','manager','approved'),
 ('director','director123','Директор','director','approved'),
 ('viewer','viewer123','Кладовщик','manager','pending');

-- Отчёты Р4.2
-- Дефицит
-- SELECT p.sku, p.name, c.name as cat, s.name as supplier, st.quantity, p.min_stock, (p.min_stock - st.quantity + 5) as need FROM products p JOIN categories c ON c.id=p.category_id JOIN suppliers s ON s.id=p.supplier_id JOIN stock st ON st.product_id=p.id WHERE st.quantity < p.min_stock ORDER BY need DESC;
-- Стоимость по категориям
-- SELECT c.name, COUNT(*), SUM(st.quantity * p.price) as value FROM products p JOIN stock st ON st.product_id=p.id JOIN categories c ON c.id=p.category_id GROUP BY c.name ORDER BY value DESC;
