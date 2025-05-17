data <- read.csv("all_apps_wide-2025-05-17.csv")

declutter <- function (data, fields) {
    rlist <- list()

    for (f in fields) {
        cols <- endsWith(colnames(data), paste0(".player.", f))
        current_values <- rep(NA_real_, nrow(data))
        current_orders <- rep(NA_real_, nrow(data))

        for (i in seq(1, nrow(data))) {
            # find matching round
            matches <- !is.na(data[i, cols])
            stopifnot(sum(matches) <= 1)

            if (sum(matches) == 1) {
                mcol <- colnames(data)[cols][matches]
                stopifnot(grepl(paste0(".", which(matches), "."), mcol, fixed = T))

                current_values[i] <- data[i, mcol]
                current_orders[i] <- which(matches)
            }
        }

        rlist[[f]] <- current_values
        rlist[[paste0(f, ".order")]] <- current_orders
    }

    data.frame(participant.code = data[, "participant.code"], rlist)
}

fielddata <- declutter(data, c("age", "siblings"))
