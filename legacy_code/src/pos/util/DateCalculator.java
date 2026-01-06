package pos.util;

import java.util.Calendar;

/**
 * Utility class for date calculations.
 * Extracted from Management class to reduce complexity.
 */
public class DateCalculator {
    
    /**
     * Calculates days between two calendar dates
     */
    public static int daysBetween(Calendar startDate, Calendar endDate) {
        Calendar start = (Calendar) startDate.clone();
        Calendar end = (Calendar) endDate.clone();
        
        // Normalize to start of day
        start.set(Calendar.HOUR_OF_DAY, 0);
        start.set(Calendar.MINUTE, 0);
        start.set(Calendar.SECOND, 0);
        start.set(Calendar.MILLISECOND, 0);
        
        end.set(Calendar.HOUR_OF_DAY, 0);
        end.set(Calendar.MINUTE, 0);
        end.set(Calendar.SECOND, 0);
        end.set(Calendar.MILLISECOND, 0);
        
        if (start.get(Calendar.YEAR) == end.get(Calendar.YEAR)) {
            return end.get(Calendar.DAY_OF_YEAR) - start.get(Calendar.DAY_OF_YEAR);
        } else {
            // Handle year boundaries
            if (end.get(Calendar.YEAR) > start.get(Calendar.YEAR)) {
                Calendar temp = start;
                start = end;
                end = temp;
            }
            
            int extraDays = 0;
            int startOriginalYearDays = start.get(Calendar.DAY_OF_YEAR);
            
            while (start.get(Calendar.YEAR) > end.get(Calendar.YEAR)) {
                start.add(Calendar.YEAR, -1);
                extraDays += start.getActualMaximum(Calendar.DAY_OF_YEAR);
            }
            
            return extraDays - end.get(Calendar.DAY_OF_YEAR) + startOriginalYearDays;
        }
    }
    
    /**
     * Calculates days between given date and today
     */
    public static int daysFromToday(Calendar date) {
        Calendar today = Calendar.getInstance();
        return daysBetween(date, today);
    }
}

