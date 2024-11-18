class ExpenseStatusMapper:
    status_mapping = {
        0: "Pending",
        1: "Approved",
        2: "Cancelled",
    }

    status_css_classes = {
        0: "bg-warning",
        1: "bg-success",
        2: "bg-danger",
    }

    @classmethod
    def get_status_text(cls, status):
        return cls.status_mapping.get(status, "Unknown")

    @classmethod
    def get_status_class(cls, status):
        return cls.status_css_classes.get(status, "bg-secondary")


class PaymentStatusMapper:
    status_mapping = {
        0: "Pending",
        1: "Approved",
        2: "Cancelled",
        3: "Payment completed",
    }

    status_css_classes = {
        0: "bg-warning",
        1: "bg-success",
        2: "bg-danger",
        3: "bg-success",
    }

    @classmethod
    def get_status_text(cls, status):
        return cls.status_mapping.get(status, "Unknown")

    @classmethod
    def get_status_class(cls, status):
        return cls.status_css_classes.get(status, "bg-secondary")
