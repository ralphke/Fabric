
CREATE PROC [dbo].[uspDimDateExtend]
	@DateTo DATE
AS
	SET NOCOUNT ON;

	DECLARE @DateFrom DATE;

	SELECT @DateFrom = DATEADD(d, 1, MAX([FullDateAlternateKey])) FROM [dbo].[DimDate];
	
	WHILE (@DateFrom <= @DateTo)
	BEGIN
		INSERT [dbo].[DimDate]
		(
			[DateKey]
			,[FullDateAlternateKey]
			,[DayNumberOfWeek]
			,[EnglishDayNameOfWeek]
			,[SpanishDayNameOfWeek]
			,[FrenchDayNameOfWeek]
			,[DayNumberOfMonth]
			,[DayNumberOfYear]
			,[WeekNumberOfYear]
			,[EnglishMonthName]
			,[SpanishMonthName]
			,[FrenchMonthName]
			,[MonthNumberOfYear]
			,[CalendarQuarter]
			,[CalendarYear]
			,[CalendarSemester]
			,[FiscalQuarter]
			,[FiscalYear]
			,[FiscalSemester]
		)
		SELECT
			((YEAR(@DateFrom) * 10000) + (MONTH(@DateFrom) * 100) + DAY(@DateFrom)) AS [DateKey]
			,@DateFrom AS [FullDateAlternateKey]
			,DATEPART(dw, @DateFrom) AS [DayNumberOfWeek]
			,CASE DATEPART(dw, @DateFrom)
				WHEN 1 THEN 'Sunday'
				WHEN 2 THEN 'Monday'
				WHEN 3 THEN 'Tuesday'
				WHEN 4 THEN 'Wednesday'
				WHEN 5 THEN 'Thursday'
				WHEN 6 THEN 'Friday'
				WHEN 7 THEN 'Saturday'
			END AS [EnglishDayNameOfWeek]
			,CASE DATEPART(dw, @DateFrom)
				WHEN 1 THEN 'Domingo'
				WHEN 2 THEN 'Lunes'
				WHEN 3 THEN 'Martes'
				WHEN 4 THEN 'Miércoles'
				WHEN 5 THEN 'Jueves'
				WHEN 6 THEN 'Viernes'
				WHEN 7 THEN 'Sábado'
			END AS [SpanishDayNameOfWeek]
			,CASE DATEPART(dw, @DateFrom)
				WHEN 1 THEN 'Dimanche'
				WHEN 2 THEN 'Lundi'
				WHEN 3 THEN 'Mardi'
				WHEN 4 THEN 'Mercredi'
				WHEN 5 THEN 'Jeudi'
				WHEN 6 THEN 'Vendredi'
				WHEN 7 THEN 'Samedi'
			END AS [FrenchDayNameOfWeek]
			,DATEPART(d, @DateFrom) AS [DayNumberOfMonth]
			,DATEPART(dy, @DateFrom) AS [DayNumberOfYear]
			,DATEPART(wk, @DateFrom) AS [WeekNumberOfYear]
			,CASE DATEPART(m, @DateFrom)
				WHEN 1 THEN 'January'
				WHEN 2 THEN 'February'
				WHEN 3 THEN 'March'
				WHEN 4 THEN 'April'
				WHEN 5 THEN 'May'
				WHEN 6 THEN 'June'
				WHEN 7 THEN 'July'
				WHEN 8 THEN 'August'
				WHEN 9 THEN 'September'
				WHEN 10 THEN 'October'
				WHEN 11 THEN 'November'
				WHEN 12 THEN 'December'
			END AS [EnglishMonthName]
			,CASE DATEPART(m, @DateFrom)
				WHEN 1 THEN 'Enero'
				WHEN 2 THEN 'Febrero'
				WHEN 3 THEN 'Marzo'
				WHEN 4 THEN 'Abril'
				WHEN 5 THEN 'Mayo'
				WHEN 6 THEN 'Junio'
				WHEN 7 THEN 'Julio'
				WHEN 8 THEN 'Agosto'
				WHEN 9 THEN 'Septiembre'
				WHEN 10 THEN 'Octubre'
				WHEN 11 THEN 'Noviembre'
				WHEN 12 THEN 'Diciembre'
			END AS [SpanishMonthName]
			,CASE DATEPART(m, @DateFrom)
				WHEN 1 THEN 'Janvier'
				WHEN 2 THEN 'Février'
				WHEN 3 THEN 'Mars'
				WHEN 4 THEN 'Avril'
				WHEN 5 THEN 'Mai'
				WHEN 6 THEN 'Juin'
				WHEN 7 THEN 'Juillet'
				WHEN 8 THEN 'Août'
				WHEN 9 THEN 'Septembre'
				WHEN 10 THEN 'Octobre'
				WHEN 11 THEN 'Novembre'
				WHEN 12 THEN 'Décembre'
			END AS [FrenchMonthName]
			,DATEPART(m, @DateFrom) AS [MonthNumberOfYear]
			,DATEPART(q, @DateFrom) AS [CalendarQuarter]
			,DATEPART(yyyy, @DateFrom) AS [CalendarYear]
			,((DATEPART(q, @DateFrom) + 1) / 2) AS [CalendarSemester]
			,DATEPART(q, DATEADD(m, 6, @DateFrom)) AS [FiscalQuarter]
			,DATEPART(yyyy, DATEADD(m, 6, @DateFrom)) AS [FiscalYear]
			,((DATEPART(q, DATEADD(m, 6, @DateFrom)) + 1) / 2) AS [FiscalSemester];

		SET @DateFrom = DATEADD(d, 1, @DateFrom);
	END;

GO

