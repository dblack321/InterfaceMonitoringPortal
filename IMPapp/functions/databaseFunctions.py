from IMPapp.functions.generalfunctions import validateUserAuthorisation
from IMPapp.models import Alert, Threshold


def _success(message):
    """Standard success response structure for database operations."""
    return {"status": "success", "message": message}


def _error(error, message):
    """Standard error response structure for database operations."""
    return {"status": "error", "error": error, "message": message}

# Database functions for Alert model
class AlertDatabaseFunctions:
    @staticmethod
    def add_alert(request, alert):
        # validate authority
        if not validateUserAuthorisation(request, 'add_alert'):
            return _error('403 Forbidden', 'You do not have permission to add alerts.')
        alert.save()
        return _success("Alert added successfully.")

    @staticmethod
    def update_alert(request, alert):
        # validate authority
        if not validateUserAuthorisation(request, 'change_alert'):
            return _error('403 Forbidden', 'You do not have permission to edit alerts.')
        alert.save()
        return _success("Alert updated successfully.")

    @staticmethod
    def delete_alert(request, alert):
        # validate authority
        if not validateUserAuthorisation(request, 'delete_alert'):
            return _error('403 Forbidden', 'You do not have permission to delete alerts.')
        alert.delete()
        return _success("Alert deleted successfully.")


# Database functions for Threshold model
class ThresholdDatabaseFunctions:
    @staticmethod
    def add_threshold(request, threshold):
        # validate authority
        if not validateUserAuthorisation(request, 'add_threshold'):
            return _error('403 Forbidden', 'You do not have permission to add thresholds.')
        threshold.save()
        return _success("Threshold added successfully.")

    @staticmethod
    def update_threshold(request, threshold):
        # validate authority
        if not validateUserAuthorisation(request, 'change_threshold'):
            return _error('403 Forbidden', 'You do not have permission to edit thresholds.')
        threshold.save()
        return _success("Threshold updated successfully.")

    @staticmethod
    def delete_threshold(request, threshold):
        # validate authority
        if not validateUserAuthorisation(request, 'delete_threshold'):
            return _error('403 Forbidden', 'You do not have permission to delete thresholds.')
        threshold.delete()
        return _success("Threshold deleted successfully.")


# Database functions for Interface model
class InterfaceDatabaseFunctions:
    @staticmethod
    def add_interface(request, interface):
        # validate authority
        if not validateUserAuthorisation(request, 'add_interface'):
            return _error('403 Forbidden', 'You do not have permission to add interfaces.')
        interface.save()
        return _success("Interface added successfully.")
    @staticmethod
    def update_interface(request, interface):
        # validate authority
        if not validateUserAuthorisation(request, 'change_interface'):
            return _error('403 Forbidden', 'You do not have permission to edit interfaces.')
        interface.save()
        return _success("Interface updated successfully.")

    @staticmethod
    def delete_interface(request, interface):
        # validate authority
        if not validateUserAuthorisation(request, 'delete_interface'):
            return _error('403 Forbidden', 'You do not have permission to delete interfaces.')
        # validate not in use
        if Alert.objects.filter(interface=interface) or Threshold.objects.filter(interface=interface):
            return _error('Interface in use', 'Interface is still assigned to a threshold or alert.')
        interface.delete()
        return _success("Interface deleted successfully.")


# Database functions for Metric model
class MetricDatabaseFunctions:
    @staticmethod
    def add_metric(request, metric):
        # validate authority
        if not validateUserAuthorisation(request, 'add_metric'):
            return _error('403 Forbidden', 'You do not have permission to add metrics.')
        metric.save()
        return _success("Metric added successfully.")

    @staticmethod
    def update_metric(request, metric):
        # validate authority
        if not validateUserAuthorisation(request, 'change_metric'):
            return _error('403 Forbidden', 'You do not have permission to edit metrics.')
        metric.save()
        return _success("Metric updated successfully.")

    @staticmethod
    def delete_metric(request, metric):
        # validate authority
        if not validateUserAuthorisation(request, 'delete_metric'):
            return _error('403 Forbidden', 'You do not have permission to delete metrics.')
        # validate not in use
        if Threshold.objects.filter(metric=metric):
            return _error('Metric in use', 'Metric is still assigned to a threshold.')
        metric.delete()
        return _success("Metric deleted successfully.")