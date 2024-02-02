-- INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(0, 'dollar', 10, 10);
-- INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(1, 'toman', 10, 10);
-- INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(2, 'lire', 10, 10);
-- INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(3, 'pound', 10, 10);
-- INSERT INTO currencyMarket(currencyID, name, buyRate, sellRate) VALUES(4, 'euro', 10, 10);
-- DROP TABLE currencymarket;
-- SELECT * FROM currencymarket;
-- easy
SELECT 
	userID, 
    userName, 
    dollarBalance, tomanBalance, lireBalance, poundBalance, euroBalance 
FROM wallet w, projschema.user u
WHERE u.userID = w.user_userID;

-- hard
SELECT 
	transactionID,
    u1.userName AS Seller,
    u2.userName AS Buyer,
    c1.name AS BaseCurrency,
    c2.name AS TargetCurrency
FROM 
	transaction t 
JOIN 
    user u1 ON t.user_sellerID = u1.userID
JOIN 
	user u2 ON t.user_buyerID1 = u2.userID
JOIN 
	currencyMarket c1 ON c1.currencyID = t.currency_fromID
JOIN
	currencyMarket c2 ON c2.currencyID = t.currency_toID
WHERE
	(t.date >'2009-01-01' AND t.date <'2010-01-01') AND 
    ((c1.name = 'toman' AND c2.name = 'dollar') OR (c1.name = 'dollar' AND c2.name = 'toman'));

-- harder 1
SELECT currency, monthNumber, buy, sell, buy+sell AS total FROM
(
 SELECT
    m.name AS currency,
    EXTRACT(MONTH FROM t.date) AS monthNumber,
    COALESCE(SUM(t2.amount), 0) AS buy,
    COALESCE(SUM(t3.amount2), 0) AS sell,
    COUNT(t2.amount) AS c1,
    COUNT(t3.amount2) AS c2
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
SELECT
    userID,
    userName,
    a1 + a2 AS `total in dollars`
FROM
    (
        SELECT
            u.userID,
            u.userName,
            SUM(t1.amount) AS a1,
            SUM(t2.amount2) AS a2
        FROM
            user u
        JOIN
            (SELECT * FROM transaction WHERE currency_fromID = 0 AND currency_toID = 1) AS t1
            ON (u.userID = t1.user_buyerID1 OR u.userID = t1.user_sellerID)
        INNER JOIN
            (SELECT * FROM transaction WHERE currency_fromID = 1 AND currency_toID = 0) AS t2
            ON (u.userID = t2.user_buyerID1 OR u.userID = t2.user_sellerID)
        GROUP BY
            u.userID, u.userName
    ) AS returned
ORDER BY 
    `total in dollars` DESC
LIMIT 5;


-- harder 3
SELECT 
	sq1.curr1 AS 'currency 1', 
    sq1.curr2 AS 'currency 2', 
    count(t1.transactionID) AS 'number of transactions',
    SUM(amount) AS 'amount in dollors',
    FLOOR(SUM(amount) / NULLIF(count(t1.transactionID),0)) AS average
FROM ( SELECT transactionID, date, amount * cm1.buyRate / cm2.buyrate AS amount, currency_fromID, currency_toID 
	FROM transaction
    JOIN currencymarket cm1 ON currency_fromID = cm1.currencyID
    JOIN currencymarket cm2 ON cm2.currencyID = 0
		WHERE date>'2009-01-01' AND date<'2011-01-01' ) AS t1
JOIN
	(SELECT m1.currencyID AS currency1, m2.currencyID AS currency2, m1.name AS curr1, m2.name AS curr2
	FROM currencymarket m1 INNER JOIN currencymarket m2 ON m1.currencyID < m2.currencyID) AS sq1
ON ((sq1.currency1 = t1.currency_toID AND sq1.currency2 = t1.currency_fromID)OR (sq1.currency2 = t1.currency_toID AND sq1.currency1 = t1.currency_fromID)) 
 GROUP BY sq1.currency1, sq1.currency2;
 
 
 
  -- ours1:user hayi ke dar hame currency ha transaction anjam dadan
SELECT
    u.userID,
    u.username
FROM
    user u
JOIN
    transaction t ON u.userID = t.user_sellerID OR u.userID = t.user_buyerID1
JOIN
    currencymarket c ON c.currencyID = t.currency_fromID OR c.currencyID = t.currency_toID
GROUP BY
    u.userID, u.username
HAVING
    COUNT(DISTINCT c.currencyID) = (SELECT COUNT(*) FROM currencymarket);
    


-- ours2: TOP10 user hayi ke bishtar az 50 transaction ba total amount bishtar az 100000 dollar !!NOT CORRECT!!
SELECT
    u.userID,
    u.username,
    COUNT(*) AS transaction_count,
    SUM(t.amount) AS total_transaction_volume
FROM
    user u
JOIN
    transaction t ON u.userID = t.user_sellerID OR u.userID = t.user_buyerID1
GROUP BY
    u.userID, u.username
HAVING
    transaction_count > 50 AND total_transaction_volume > 100000
ORDER BY
    total_transaction_volume DESC
LIMIT 10;


-- ours3: TOP10
SELECT
    u.userID,
    u.username,
    COUNT(*) AS transaction_count
FROM
    user u
JOIN
    transaction t1 ON u.userID = t1.user_buyerID1
JOIN
    transaction t2 ON u.userID = t2.user_sellerID
WHERE
    t1.currency_fromID = t2.currency_toID
    AND t1.currency_toID = t2.currency_fromID
GROUP BY
    u.userID, u.username
ORDER BY
    transaction_count DESC
LIMIT 10;
--- SELECT * FROM transaction WHERE user_buyerID1=3696 OR user_sellerID=3696;
--ours4:har arz chand bar moamele shode
SELECT curr.name,  COUNT(curr.currencyID) AS traded
FROM currencymarket curr
JOIN transaction t ON (curr.currencyID = t.currency_fromID OR curr.currencyID = t.currency_toID)
GROUP BY curr.currencyID;

--ours5: useri ke az hame bishtar dollar forookhteh
SELECT u.userID, SUM(t.amount) AS 'max selling dollar' 
FROM user u
JOIN transaction t on u.userID = t.user_sellerID
WHERE t.currency_fromID = 1
GROUP BY u.userID
HAVING SUM(t.amount)> ALL(SELECT SUM(t2.amount)
                      FROM user u2
                      JOIN transaction t2 on u2.userID = t2.user_sellerID
                      WHERE t2.currency_fromID = 1 AND u2.userID != u.userID
                      GROUP BY u2.userID);

--ours6: user hayi ke lire moamele nakardand
SELECT u.userID AS ID, u.userName AS name
FROM user u
WHERE u.userID NOT IN(
    SELECT u2.userID
    FROM user u2
    JOIN transaction t on (u2.userID = t.user_sellerID OR u2.userID = t.user_buyerID1)
    WHERE t.currency_fromID = 3 OR t.currency_toID = 3);
--ours7:user hayi ke faqat ba yek joft arz moamele anjam dadand
SELECT temp.userID, temp.userName, temp.CID
FROM
((SELECT u.userID, u.userName, t.currency_fromID AS CID
FROM user u
JOIN transaction t ON (t.user_sellerID = u.userID)
GROUP BY u.userID)
UNION
(SELECT u.userID, u.userName, t.currency_toID AS CID
FROM user u
JOIN transaction t ON (t.user_buyerID1 = u.userID)
GROUP BY u.userID)) AS temp
GROUP BY temp.userID
HAVING COUNT(DISTINCT temp.CID) = 2;
--ours8: tedad moamele beyn joft user hayi ke hadaqal yek moamele dashtand
SELECT t.user_sellerID AS sellerID, t.user_buyerID1 AS buyerID
, u1.userName AS sellerName, u2.userName AS buyerName, COUNT(t.transactionID) AS transactionCount 
FROM transaction t 
JOIN user u1 ON t.user_sellerID = u1.userID 
JOIN user u2 ON t.user_buyerID1 = u2.userID 
GROUP BY sellerID, buyerID;
--ours9: user hayi ke hadaksar 2 moamele anjam dadand
SELECT userID, username
FROM user 
WHERE userID NOT IN(
SELECT userID
FROM user
JOIN transaction ON userID = user_sellerID OR userID = user_buyerID1
GROUP BY userID
HAVING COUNT(transactionID)>2);
--ours10: user hayi ke ba hame joft arz haye momken moamele anjam dadand
SELECT u.userID, u.userName
FROM user u
JOIN transaction t ON (u.userID = t.user_sellerID OR u.userID = t.user_buyerID1) 
GROUP BY u.userID
HAVING (COUNT(DISTINCT t.currency_fromID) = 5) AND (COUNT(DISTINCT t.currency_toID) = 5);