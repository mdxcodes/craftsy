/// Represents a commerce channel status for display in the UI.
class ChannelStatus {
  final String channel;
  final String status;
  final String label;
  final String icon;
  final String color;
  final bool isConnected;
  final bool canPublish;
  final List<String> missingRequirements;

  const ChannelStatus({
    required this.channel,
    required this.status,
    required this.label,
    required this.icon,
    required this.color,
    required this.isConnected,
    required this.canPublish,
    this.missingRequirements = const [],
  });

  factory ChannelStatus.fromJson(Map<String, dynamic> json) {
    return ChannelStatus(
      channel: json['channel'] as String? ?? '',
      status: json['status'] as String? ?? '',
      label: json['label'] as String? ?? '',
      icon: json['icon'] as String? ?? '',
      color: json['color'] as String? ?? 'grey',
      isConnected: json['is_connected'] as bool? ?? false,
      canPublish: json['can_publish'] as bool? ?? false,
      missingRequirements:
          (json['missing_requirements'] as List<dynamic>?)
              ?.map((e) => e.toString())
              .toList() ??
          [],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'channel': channel,
      'status': status,
      'label': label,
      'icon': icon,
      'color': color,
      'is_connected': isConnected,
      'can_publish': canPublish,
      'missing_requirements': missingRequirements,
    };
  }

  /// Whether this channel shows a green "live" state.
  bool get isLive => isConnected && status == 'active' || status == 'published';

  /// Whether this channel needs user information.
  bool get needsInfo => status == 'needs_information';

  /// Whether this channel is not yet connected.
  bool get isNotConnected =>
      status == 'not_connected' || status == 'disconnected';

  /// Whether this channel has failed.
  bool get hasFailed => status == 'failed' || status == 'rejected';

  /// Whether this channel is pending.
  bool get isPending => status == 'pending';

  /// Status display text for the UI.
  String get displayStatus {
    switch (status) {
      case 'active':
      case 'published':
        return 'Live';
      case 'draft':
        return 'Draft';
      case 'not_connected':
        return 'Not Connected';
      case 'needs_information':
        return 'Needs Information';
      case 'ready':
        return 'Ready';
      case 'pending':
        return 'Pending';
      case 'failed':
        return 'Failed';
      case 'rejected':
        return 'Rejected';
      case 'disconnected':
        return 'Disconnected';
      case 'eligibility_required':
        return 'Eligibility Required';
      default:
        return status
            .replaceAll('_', ' ')
            .split(' ')
            .map((w) => w[0].toUpperCase() + w.substring(1))
            .join(' ');
    }
  }
}
