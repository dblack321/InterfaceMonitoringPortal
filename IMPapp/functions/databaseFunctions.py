
# Database functions for Alert model
from urllib import request, response

from IMPapp.functions.generalfunctions import validateUserAuthorisation
from IMPapp.models import Alert, Threshold

# Database functions for Alert model
class AlertDatabaseFunctions:
    @staticmethod
    def add_alert(request, alert):
        # validate authority
        if not validateUserAuthorisation(request, 'add_alert'):
            return response.error('403 Forbidden', 'You do not have permission to add alerts.')
        alert.save()
        return response.success("Alert added successfully.")

    @staticmethod
    def update_alert(request, alert):
        # validate authority
        if not validateUserAuthorisation(request, 'change_alert'):
            return response.error('403 Forbidden', 'You do not have permission to edit alerts.')
        alert.save()
        return response.success("Alert updated successfully.")

    @staticmethod
    def delete_alert(request, alert):
        # validate authority
        if not validateUserAuthorisation(request, 'delete_alert'):
            return response.error('403 Forbidden', 'You do not have permission to delete alerts.')
        alert.delete()
        return response.success("Alert deleted successfully.")


# Database functions for Threshold model
class ThresholdDatabaseFunctions:
    @staticmethod
    def add_threshold(request, threshold):
        # validate authority
        if not validateUserAuthorisation(request, 'add_threshold'):
            return response.error('403 Forbidden', 'You do not have permission to add thresholds.')
        threshold.save()
        return response.success("Threshold added successfully.")

    @staticmethod
    def update_threshold(request, threshold):
        # validate authority
        if not validateUserAuthorisation(request, 'change_threshold'):
            return response.error('403 Forbidden', 'You do not have permission to edit thresholds.')
        threshold.save()
        return response.success("Threshold updated successfully.")

    @staticmethod
    def delete_threshold(request, threshold):
        # validate authority
        if not validateUserAuthorisation(request, 'delete_threshold'):
            return response.error('403 Forbidden', 'You do not have permission to delete thresholds.')
        threshold.delete()
        return response.success("Threshold deleted successfully.")


# Database functions for Interface model
class InterfaceDatabaseFunctions:
    @staticmethod
    def add_interface(request, interface):
        # validate authority
        if not validateUserAuthorisation(request, 'add_interface'):
            return response.error('403 Forbidden', 'You do not have permission to add interfaces.')
        interface.save()
        return response.success("Interface added successfully.")
    @staticmethod
    def update_interface(request, interface):
        # validate authority
        if not validateUserAuthorisation(request, 'change_interface'):
            return response.error('403 Forbidden', 'You do not have permission to edit interfaces.')
        interface.save()
        return response.success("Interface updated successfully.")

    @staticmethod
    def delete_interface(request, interface):
        # validate authority
        if not validateUserAuthorisation(request, 'delete_interface'):
            return response.error('403 Forbidden', 'You do not have permission to delete interfaces.')
        # validate not in use
        if Alert.objects.filter(interface=interface) or Threshold.objects.filter(interface=interface):
            return response.error('Interface in use', 'Interface is still assigned to a threshold or alert.')
        interface.delete()
        return response.success("Interface deleted successfully.")


# Database functions for Metric model
class MetricDatabaseFunctions:
    @staticmethod
    def add_metric(request, metric):
        # validate authority
        if not validateUserAuthorisation(request, 'add_metric'):
            return response.error('403 Forbidden', 'You do not have permission to add metrics.')
        metric.save()
        return response.success("Metric added successfully.")

    @staticmethod
    def update_metric(metric):
        # validate authority
        if not validateUserAuthorisation(request, 'change_metric'):
            return response.error('403 Forbidden', 'You do not have permission to edit metrics.')
        metric.save()
        return response.success("Metric updated successfully.")

    @staticmethod
    def delete_metric(request, metric):
        # validate authority
        if not validateUserAuthorisation(request, 'delete_metric'):
            return response.error('403 Forbidden', 'You do not have permission to delete metrics.')
        # validate not in use
        if Threshold.objects.filter(metric=metric):
            return response.error('Metric in use', 'Metric is still assigned to a threshold.')
        metric.delete()
        return response.success("Metric deleted successfully.")