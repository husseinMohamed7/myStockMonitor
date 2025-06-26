-- sql statments to make datasets
-- summary_financials
CREATE OR REPLACE VIEW public.summary_financials AS
SELECT
  (SELECT SUM("CashFlow") FROM public.transactions WHERE "Type" = 'Deposit') AS total_deposits,

  (SELECT SUM("CashFlow") FROM public.transactions WHERE "Type" = 'Withdrawal') AS total_withdrawals,

  (SELECT SUM("CashFlow") FROM public.transactions WHERE "Type" = 'Dividend') AS total_dividends,

  (SELECT SUM("CashFlow") FROM public.transactions WHERE "Type" = 'Bonus') AS total_bonus,

  (SELECT SUM(amount * price) FROM public.portfolio_status) AS current_portfolio_value,

  (SELECT SUM("CashFlow") FROM public.transactions WHERE "Type" = 'Fee') AS current_fee;

-- net profit from the summary_financials view
SELECT
  SUM("current_portfolio_value") -  SUM("total_withdrawals")  - SUM("total_deposits")AS net_profit
FROM public.summary_financials;
