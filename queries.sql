-- INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(0, 'dollar', 10, 10);
-- INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(1, 'toman', 10, 10);
-- INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(2, 'lire', 10, 10);
-- INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(3, 'pound', 10, 10);
-- INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(4, 'euro', 10, 10);
-- DROP TABLE currencymarket;
-- SELECT * FROM currencymarket;
-- easy: DONE
-- SELECT 
-- 	userID, 
--     userName, 
--     dollarBalance, tomanBalance, lireBalance, poundBalance, euroBalance 
-- FROM wallet w, projschema.user u
-- WHERE u.userID = w.user_userID;

-- hard: DONE
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
-- SELECT m.name AS currency, 
-- 	EXTRACT(MONTH FROM t.date) AS monthNumber, 
--     (SELECT SUM(amount) FROM (SELECT user_buyerID1, amount FROM transaction t2 WHERE t2.currency_fromID=m.currencyID)) AS buy,  
--     (SELECT SUM(amount2)FROM (SELECT user_sellerID, amount2 FROM transaction t3 WHERE t3.currrency_toID=m.currencyID)) AS sell
-- FROM transaction t, currencyMarket m
-- WHERE EXTRACT(YEAR FROM t.date) = '2009'
-- -- total = SELECT IF(m.currencyID = t.currency_fromID, t.amount, amount2) FROM transaction
-- GROUP BY currency, monthNumber
-- ORDER by currency
-- ;

SELECT currency, monthNumber, buy, sell, buy+sell AS total FROM
(
 SELECT
    m.name AS currency,
    EXTRACT(MONTH FROM t.date) AS monthNumber,
    COALESCE(SUM(t2.amount), 0) AS buy,
    COALESCE(SUM(t3.amount2), 0) AS sell
FROM
    currencyMarket m
JOIN
    transaction t ON m.currencyID = t.currency_fromID
LEFT JOIN
    (SELECT user_buyerID1, amount, currency_fromID FROM transaction WHERE EXTRACT(YEAR FROM date) = 2009) AS t2
    ON m.currencyID = t2.currency_fromID
LEFT JOIN
    (SELECT user_sellerID, amount2, currency_toID FROM transaction WHERE EXTRACT(YEAR FROM date) = 2009) AS t3
    ON m.currencyID = t3.currency_toID
WHERE
    EXTRACT(YEAR FROM t.date) = 2009
GROUP BY
    currency, monthNumber
    ) AS returned 
ORDER BY
    currency, monthNumber;

-- harder 2

