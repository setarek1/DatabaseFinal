-- INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(0, 'dollar', 10, 10);
-- INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(1, 'toman', 10, 10);
-- INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(2, 'lire', 10, 10);
-- INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(3, 'pound', 10, 10);
-- INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(4, 'euro', 10, 10);
-- DROP TABLE currencymarket;
-- SELECT * FROM currencymarket;
-- -- 1- easy
-- SELECT 
-- 	userID, 
--     userName, 
--     dollarBalance, tomanBalance, lireBalance, poundBalance, euroBalance 
-- FROM wallet w, projschema.user u
-- WHERE u.userID = w.user_userID;

-- hard
-- SELECT 
-- 	transactionID,
--     u1.userName AS Seller,
--     u2.userName AS Buyer,
--     c1.name AS BaseCurrency,
--     c2.name AS TargetCurrency
-- FROM 
-- 	transaction t 
-- JOIN 
--     user u1 ON t.user_sellerID = u1.userID
-- JOIN 
-- 	user u2 ON t.user_buyerID1 - u2.userID
-- JOIN 
-- 	currencyMarket c1 ON c1.currencyID = t.currency_fromID
-- JOIN
-- 	currencyMarket c2 ON c2.currencyID = t.currency_toID
-- WHERE
-- 	(t.date >'2009-01-01' AND t.date <'2010-01-01') AND 
--     ((c1.name = 'toman' AND c2.name = 'dollar') OR (c1.name = 'dollar' AND c2.name = 'toman'));

-- harder 1
-- SELECT currencymarket.name AS currency, EXTRACT(MONTH FROM transaction.date) AS month, COUNT(*) AS transactionCount, SUM(tran);
-- SELECT name AS currency, 
-- EXTRACT(MONTH FROM transaction.date) AS month, 
-- COUNT(*) AS 'number of transactions'
-- FROM 



-- harder
-- total = total buy + total sell
SELECT amount FROM transaction 
WHERE user_buyerID1 = u.userID;
SELECT amount2 FROM transaction 
WHERE user_sellerID = u.userID;
DECLARE totalBuy, totalSell FLOAT;
SELECT SUM(amount) INTO totalBuy
SELECT 
	userName ,SUM (totalAmount) AS 'total amount in dollors'

FROM u;
    
	
