import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import main

class TestScaleResource(unittest.TestCase):

    @patch("main.client.CustomObjectsApi")
    @patch("main.client.AppsV1Api")
    def test_scale_resource(self, mock_apps_api, mock_custom_api):
        # Mock CustomObjectsApi response
        mock_crd = {
            'items': [
                {
                    'spec': {
                        'targetDeployment': 'test-deployment',
                        'scalePercentage': 20,
                        'scheduleTime': '08:50',
                        'duration': '30'
                    }
                }
            ]
        }
        mock_custom_api.return_value.list_namespaced_custom_object.return_value = mock_crd

        # Mock AppsV1Api response
        deployment = MagicMock()
        deployment.spec.replicas = 5
        mock_apps_api.return_value.read_namespaced_deployment.return_value = deployment

        # Patch datetime
        test_time = datetime.strptime('08:50', "%H:%M")
        with patch("main.datetime") as mock_datetime:
            mock_datetime.now.return_value = test_time
            mock_datetime.strptime.side_effect = lambda *args, **kw: datetime.strptime(*args, **kw)

            # Run scale_resource for a short duration
            with patch("main.time.sleep", side_effect=InterruptedError):
                try:
                    main.scale_resource()
                except InterruptedError:
                    pass

        # Check deployment was scaled up
        mock_apps_api.return_value.replace_namespaced_deployment.assert_any_call(
            'test-deployment',
            'default',
            deployment
        )
        self.assertEqual(deployment.spec.replicas, 6)  # 20% increase of 5 is 6

if __name__ == "__main__":
    unittest.main()
